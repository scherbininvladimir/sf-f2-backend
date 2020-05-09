from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import (
    QuestionnaireSerializer, 
    QuestionnaireContentSerializer, 
    QuestionnaireRusultSerilizer, 
    AdminResultSerializer,
)
from rest_framework import generics  

from .models import Question, Questionnaire, QuestionnaireResult, QuestionnaireContent
from django.contrib.auth.models import User  


class QuestionnaireList(generics.ListAPIView):

    serializer_class = QuestionnaireSerializer

    def get_queryset(self):
        return Questionnaire.objects.filter(target_users=self.request.user)


class QuestionnaireContentList(generics.ListAPIView):
    
    serializer_class = QuestionnaireContentSerializer

    def get_queryset(self):
        questionnaire = get_object_or_404(Questionnaire, target_users=self.request.user, id=self.kwargs['pk'])
        return get_list_or_404(QuestionnaireContent, questionnaire=questionnaire)


class ResultDetail(generics.RetrieveUpdateAPIView):
    
    serializer_class = QuestionnaireRusultSerilizer

    def get_object(self):
        questionnaire_content = get_object_or_404(QuestionnaireContent, pk=self.kwargs['questionnaire_content_pk'])
        return QuestionnaireResult.objects.filter(questionnaire_content=questionnaire_content, user=self.request.user).first()


class ResultCreate(generics.CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = QuestionnaireRusultSerilizer


class Statistics(generics.ListAPIView):

    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

class StatisticsDetail(generics.ListAPIView):

    queryset = QuestionnaireResult.objects.all()
    serializer_class = AdminResultSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        questionnaire = get_object_or_404(Questionnaire, pk=self.kwargs['questionnaire_pk'])
        questionnaire_content = QuestionnaireContent.objects.filter(questionnaire=questionnaire)
        return QuestionnaireResult.objects.filter(questionnaire_content__in=questionnaire_content, user=user)
