from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Question, Response, Questionnaire, QuestionnaireContent, QuestionnaireResult


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


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


class QuestionnaireContentSerializer(serializers.ModelSerializer):

    question = QuestionSerializer()
    
    class Meta:
        model = QuestionnaireContent
        fields = ('id', 'question', 'time_to_answer', 'answer_weight')


class QuestionnaireSerializer(serializers.ModelSerializer):
    
    questions = QuestionnaireContentSerializer(source='questionnairecontent_set', many=True)

    class Meta:
        model = Questionnaire
        fields = ('id', 'title', 'start_date', 'end_date', 'questions', 'target_users', 'allow_answer_modify')
    

class QuestionnaireRusultSerilizer(serializers.ModelSerializer):
    
    class Meta:
        model = QuestionnaireResult
        fields = '__all__'

