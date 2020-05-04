from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import QuestionSerializer, QuestionnaireSerializer, QuestionnaireRusultSerilizer, UserSerializer
from rest_framework import generics  

from .models import Question, Questionnaire, QuestionnaireResult, QuestionnaireContent
from django.contrib.auth.models import User  


class UserList(generics.ListAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer


class QuestionCreate(generics.ListCreateAPIView):  
    
    queryset = Question.objects.all()  
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):  
    
    queryset = Question.objects.all()  
    serializer_class = QuestionSerializer


class QuestionnaireList(generics.ListAPIView):

    serializer_class = QuestionnaireSerializer

    def get_queryset(self):
        return Questionnaire.objects.filter(target_users=self.request.user)


class QuestionnaireDetail(generics.RetrieveAPIView):
    
    serializer_class = QuestionnaireSerializer

    def get_object(self):
        if self.request.user.is_staff:
            return get_object_or_404(Questionnaire, id=self.kwargs['pk'])
        else:
            return get_object_or_404(Questionnaire, target_users=self.request.user, id=self.kwargs['pk'])        


class ResultDetail(generics.RetrieveUpdateAPIView):
    
    serializer_class = QuestionnaireRusultSerilizer

    def get_object(self):
        questionnaire_content = get_object_or_404(QuestionnaireContent, pk=self.kwargs['questionnaire_content_pk'])
        return QuestionnaireResult.objects.filter(questionnaire_content=questionnaire_content, user=self.request.user).first()


class ResultCreate(generics.CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = QuestionnaireRusultSerilizer


class ResultList(generics.ListAPIView):

    serializer_class = QuestionnaireRusultSerilizer

    def get_queryset(self):
        questionnaire = get_object_or_404(Questionnaire, pk=self.kwargs['questionnaire_pk'])
        questionnaire_content = QuestionnaireContent.objects.filter(questionnaire=questionnaire)
        return QuestionnaireResult.objects.filter(questionnaire_content__in=questionnaire_content, user=self.request.user)

