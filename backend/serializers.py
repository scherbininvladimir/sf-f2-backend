from collections import Counter
import redis

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.contrib.auth.models import User
from .models import Question, Response, Questionnaire, QuestionnaireContent, QuestionnaireResult

from inquirer_backend.settings import REDIS_HOST

r = redis.Redis(host=REDIS_HOST, port=6379, db=0)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'is_staff')


class ResponseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Response
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):  
    
    response = ResponseSerializer(many=True)
    
    class Meta:  
        model = Question  
        fields = (
            'title', 
            'content', 
            'answers_number', 
            'question_type', 
            'response', 
        )


class QuestionnaireSerializer(serializers.ModelSerializer):

    number_of_questions = serializers.SerializerMethodField('get_number_of_questions')
    number_of_answerred_questions = serializers.SerializerMethodField('get_number_of_answerred_questions')
    users_scores = serializers.SerializerMethodField() 

    def get_users_scores(self, obj):
        questionnaire_content = QuestionnaireContent.objects.filter(questionnaire = obj)
        results = QuestionnaireResult.objects.filter(questionnaire_content__in=questionnaire_content)
        counter = Counter()
        response = {
            "your_score": 0,
            "detail_stat": [],
            "generalized_stat": [],
        }
        for r in results:
            counter[r.user.id] += r.score
        for key in counter:
            if self.context.get('request').user.is_staff: # Если пользователь - администратор, передаем результаты по каждому пльзователю, иначе только обобщенные данные
                user = User.objects.get(pk=key)
                response["detail_stat"].append({"user_id": user.id, "first_name": user.first_name, "last_name": user.last_name, "scores": counter[key]})
            if key == self.context.get('request').user.id: 
                response["your_score"] = counter[key]
            else:
                response["generalized_stat"].append(counter[key])
        return response

    def get_number_of_questions(self, obj):
        return obj.questions.count()

    def get_number_of_answerred_questions(self, obj):
        questonnnaire_content = QuestionnaireContent.objects.filter(questionnaire = obj)
        resluts = QuestionnaireResult.objects.filter(
            questionnaire_content__in = questonnnaire_content, 
            user=self.context.get('request').user
        ).exclude(answer=[])
        return resluts.count()

    class Meta:
        model = Questionnaire
        fields = (
            'id', 
            'title', 
            'start_date', 
            'end_date', 
            'description', 
            'allow_answer_modify', 
            'time_to_answer',
            'questions', 
            'isOpen',
            'number_of_questions',
            'number_of_answerred_questions',
            'users_scores',
        )
    

class QuestionnaireContentSerializer(serializers.ModelSerializer):

    question = QuestionSerializer()
    questionnaire = QuestionnaireSerializer()
    
    class Meta:
        model = QuestionnaireContent
        fields = ('id', 'questionnaire', 'question', 'time_to_answer', 'answer_weight')


class QuestionnaireRusultSerilizer(serializers.ModelSerializer):

    def create(self, validated_data):
        questionnaire = validated_data["questionnaire_content"].questionnaire
        question = validated_data["questionnaire_content"]
        questionnaire_time_to_answer = questionnaire.time_to_answer
        queston_time_to_answer = question.time_to_answer
        user = validated_data["user"]
        questionnaire_content = QuestionnaireContent.objects.filter(questionnaire=questionnaire)
        is_questionnaire_in_results = QuestionnaireResult.objects.filter(user=user, questionnaire_content__in=questionnaire_content)
        if questionnaire_time_to_answer and not is_questionnaire_in_results:
            r.set(
                f'{validated_data["user"].id}/{questionnaire.id}',
                questionnaire_time_to_answer,
                ex=questionnaire_time_to_answer
            )
        if queston_time_to_answer:
            r.set(
                f'{validated_data["user"].id}/{validated_data["questionnaire_content"].id}',
                queston_time_to_answer, 
                ex=queston_time_to_answer
            )
        return QuestionnaireResult.objects.create(**validated_data)

    def validate_answer(self, value):
        if self.instance:
            need_to_check = self.instance.questionnaire_content.time_to_answer
            is_time_out = not r.get(f'{self.instance.user.id}/{self.instance.questionnaire_content.id}')
            if need_to_check and is_time_out:
                raise serializers.ValidationError("Время вышло.")
        return value
                
    class Meta:
        model = QuestionnaireResult
        fields = ('id', 'answer', 'user', 'questionnaire_content')
        validators = [
            UniqueTogetherValidator(
                queryset=QuestionnaireResult.objects.all(),
                fields=['user', 'questionnaire_content']
            )
        ]


class AdminResultSerializer(serializers.ModelSerializer):

    questionnaire_content = QuestionnaireContentSerializer()
    user = UserSerializer()
    class Meta:
        model = QuestionnaireResult
        fields = ('id', 'answer', 'user', 'questionnaire_content', 'score')
