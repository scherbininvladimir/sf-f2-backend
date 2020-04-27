from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import QuestionSerializer, QuestionnaireSerializer, QuestionnaireRusultSerilizer, UserSerializer
from rest_framework import generics  

from .models import Question, Questionnaire, QuestionnaireResult, QuestionnaireContent
from django.contrib.auth.models import User  


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class QuestionList(generics.ListCreateAPIView):  
    queryset = Question.objects.all()  
    serializer_class = QuestionSerializer

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):  
    queryset = Question.objects.all()  
    serializer_class = QuestionSerializer

class QuestionnaireList(generics.ListCreateAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

class QuestionnaireDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer


class ResultDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionnaireRusultSerilizer

    def get_object(self):
        questionnaire_content = get_object_or_404(QuestionnaireContent, pk=self.kwargs['questionnaire_content_pk'])
        user = get_object_or_404(User, id=self.kwargs['user_pk'])
        return get_object_or_404(QuestionnaireResult, questionnaire_content=questionnaire_content, user=user)

class QuestionnaireResultList(generics.ListCreateAPIView):
    
    serializer_class = QuestionnaireRusultSerilizer

    def get_queryset(self):
        questionnaire = get_object_or_404(Questionnaire, pk=self.kwargs['questionnaire_pk'])
        questionnaire_contents = QuestionnaireContent.objects.filter(questionnaire=questionnaire)
        return QuestionnaireResult.objects.filter(questionnaire_content__in=questionnaire_contents)
        
    

class QuestionnaireUserResultList(generics.ListCreateAPIView):
    
    serializer_class = QuestionnaireRusultSerilizer
    
    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs['user_pk'])
        return QuestionnaireResult.objects.filter(user=user)

