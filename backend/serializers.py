from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Question, Questionnaire, QuestionnaireContent, QuestionnaireResult


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class QuestionSerializer(serializers.ModelSerializer):  
    
    class Meta:  
        model = Question  
        fields = '__all__'


class QuestionnaireContentSerializer(serializers.ModelSerializer):

    question = QuestionSerializer()

    class Meta:
        model = QuestionnaireContent
        fields = ('id', 'question', 'time_to_answer', 'answer_weight')


class QuestionnaireSerializer(serializers.ModelSerializer):
    
    questions = QuestionnaireContentSerializer(source='questionnairecontent_set', many=True)

    class Meta:
        model = Questionnaire
        fields = ('id', 'title', 'start_date', 'end_date', 'questions', 'target_users')
    
    def create(self, validated_data):
        questionnaire_content_set = validated_data.pop('questionnaire_content_set')
        questionnaire = Questionnaire.objects.create(
            title=validated_data['title'],
            time_to_live=validated_data['time_to_live'],
        )
        return questionnaire

    def update(self, instance, validated_data):
        instance.name = validated_data.get('title', instance.title)
        instance.target_users.set(validated_data.get('target_users', instance.target_users))
        instance.save()

        QuestionnaireContent.objects.filter(questionnaire=instance).delete()
        for questionnaire_content_od in validated_data['questionnairecontent_set']:
            questionnaire_content = dict(questionnaire_content_od)
            QuestionnaireContent.objects.create(
                questionnaire=instance, 
                question=questionnaire_content['question'], 
                time_to_answer=questionnaire_content['time_to_answer'], 
                answer_weight=questionnaire_content['answer_weight']
                )
        return instance


class QuestionnaireRusultSerilizer(serializers.ModelSerializer):
    
    class Meta:
        model = QuestionnaireResult
        fields = '__all__'

