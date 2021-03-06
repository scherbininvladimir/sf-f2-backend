import datetime

from collections import Counter
import redis

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.core.exceptions import ObjectDoesNotExist
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
        fields = ('response_option', 'isCorrect', 'answer_weight',)


class QuestionSerializer(serializers.ModelSerializer):  
    
    response = ResponseSerializer(many=True)
    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        if obj.picture:
            return obj.picture.url
        return None

    def create(self, validated_data):
        response_data = validated_data.pop('response')
        question = Question.objects.create(
            title = validated_data.get('title'),
            content = validated_data.get('content'),
            answers_number = validated_data.get('answers_number'),
            question_type = validated_data.get('question_type')
        )
        for response in response_data:
            Response.objects.create(question=question, **response)
        return question
    

    def update(self, instance, validated_data):
        response_data = validated_data.pop('response')

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.answers_number = validated_data.get('answers_number', instance.answers_number)
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.save()

        response_options = [response.response_option for response in Response.objects.filter(question=instance)]
        response_options_form = [response["response_option"] for response in response_data]
        
        response_options_for_update = set(response_options).intersection(set(response_options_form))
        response_options_for_delete = set(response_options).difference(set(response_options_form))

        for response_form in response_data:
            if response_form["response_option"] in response_options_for_update:
                response = Response.objects.get(question=instance, response_option=response_form["response_option"])
                response.response_option = response_form.get('response_option', response.response_option)
                response.isCorrect = response_form.get('isCorrect', response.isCorrect)
                response.answer_weight = response_form.get('answer_weight', response.answer_weight)
                response.save()
            else:
                Response.objects.create(question=instance, **response_form)
        
        Response.objects.filter(question=instance, response_option__in=response_options_for_delete).delete()
        
        return instance
    
    class Meta:  
        model = Question  
        fields = (
            'id',
            'title', 
            'content', 
            'picture',
            'answers_number', 
            'question_type', 
            'response', 
        )


class QuestionnaireSerializer(serializers.ModelSerializer):

    number_of_questions = serializers.SerializerMethodField()
    number_of_answerred_questions = serializers.SerializerMethodField()
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
    
    def create(self, validated_data):
        print(validated_data)
        questions_data = validated_data.pop('questions')
        questionnaire = Questionnaire.objects.create(
            title = validated_data.get('title'),
            start_date = validated_data.get('start_date'),
            end_date = validated_data.get('end_date'),
            description = validated_data.get('description'),
            time_to_answer = validated_data.get('time_to_answer'),
            allow_answer_modify = validated_data.get('allow_answer_modify'),
        )
        questionnaire.target_users.set(validated_data.get('target_users'))
        for question_in_questionnaire in questions_data:
            question = Question.objects.get(id=question_in_questionnaire["question"]["id"])
            QuestionnaireContent.objects.create(
                question=question,
                questionnaire=questionnaire, 
                time_to_answer = question_in_questionnaire["time_to_answer"],
                answer_weight = question_in_questionnaire["answer_weight"],
            )
        return questionnaire
    
    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions')
        instance.title = validated_data.get('title', instance.title)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.description = validated_data.get('description', instance.description)
        instance.allow_answer_modify = validated_data.get('allow_answer_modify', instance.allow_answer_modify)
        instance.time_to_answer = validated_data.get('time_to_answer', instance.time_to_answer)
        instance.target_users.clear()
        instance.target_users.set(validated_data.get('target_users'))
        instance.save()
        
        questions_in_questionnaire_db = [q.id for q in QuestionnaireContent.objects.filter(questionnaire=instance)]
        questions_in_questionnaire_form = [q.get("id") for q in questions_data]
        
        questions_in_questionnaire_for_update = set(questions_in_questionnaire_db).intersection(set(questions_in_questionnaire_form))
        questions_in_questionnaire_delete = set(questions_in_questionnaire_db).difference(set(questions_in_questionnaire_form))
        
        for question_in_questionnaire_form in questions_data:
            if question_in_questionnaire_form.get("id") in questions_in_questionnaire_for_update:
                questions_in_questionnaire = QuestionnaireContent.objects.get(id=question_in_questionnaire_form["id"])
                question = Question.objects.get(id=question_in_questionnaire_form["question"]["id"])                
                questions_in_questionnaire.question = question                
                questions_in_questionnaire.time_to_answer = question_in_questionnaire_form.get('time_to_answer', questions_in_questionnaire.time_to_answer)
                questions_in_questionnaire.answer_weight = question_in_questionnaire_form.get('answer_weight', questions_in_questionnaire.answer_weight)
                questions_in_questionnaire.save()
            else:
                question = Question.objects.get(id=question_in_questionnaire_form["question"]["id"])
                QuestionnaireContent.objects.create(question=question, questionnaire=instance)
        
        QuestionnaireContent.objects.filter(id__in=questions_in_questionnaire_delete).delete()

        return instance
    
    def to_representation(self, instance):
        q = super().to_representation(instance)
        q['questions'] = []
        for question_in_questionnaire in QuestionnaireContent.objects.filter(questionnaire=instance):
            q['questions'].append({
                "id": question_in_questionnaire.id,
                "question": {
                    "id": question_in_questionnaire.question.id,
                    "title": question_in_questionnaire.question.title,
                },
                "time_to_answer": question_in_questionnaire.time_to_answer,
                "answer_weight": question_in_questionnaire.answer_weight,
            })
        return q
    
    def to_internal_value(self, data):
        q = super().to_internal_value(data)
        q['questions'] = data["questions"]
        return q            

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
            'target_users',
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
        user = validated_data["user"]
        questionnaire_content = QuestionnaireContent.objects.filter(questionnaire=questionnaire)
        is_questionnaire_in_results = QuestionnaireResult.objects.filter(user=user, questionnaire_content__in=questionnaire_content)
        if questionnaire.time_to_answer and not is_questionnaire_in_results:
            r.set(
                f'{validated_data["user"].id}/{questionnaire.id}',
                questionnaire.time_to_answer,
                ex=questionnaire.time_to_answer
            )
        if question.time_to_answer:
            r.set(
                f'{validated_data["user"].id}/{validated_data["questionnaire_content"].id}',
                question.time_to_answer, 
                ex=question.time_to_answer
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
