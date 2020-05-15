from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import (
    QuestionnaireSerializer, 
    QuestionnaireContentSerializer, 
    QuestionnaireRusultSerilizer, 
    AdminResultSerializer,
    QuestionSerializer,
    UserSerializer,
)
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Question, Questionnaire, QuestionnaireResult, QuestionnaireContent
from django.contrib.auth.models import User  


class AdminUsers(generics.ListAPIView):

    permission_classes = [IsAdminUser]
    
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminQuestionList(generics.ListCreateAPIView):

    permission_classes = [IsAdminUser]
    
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AdminQuestionDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminUser]
    
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class PictureUploadView(APIView):

    def put(self, request, filename, question_id, format=None):
        picture = request.data['file']
        print(picture)
        question = get_object_or_404(Question, id=question_id)
        question.picture = picture
        question.save()
        return Response(status=204)


class AdminQuestionnaireList(generics.ListCreateAPIView):

    permission_classes = [IsAdminUser]

    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer


class AdminQuestionnaireDetail(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminUser]
    
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer


class AdminResults(generics.ListAPIView):

    permission_classes = [IsAdminUser]

    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

class AdminResultDetail(generics.ListAPIView):

    permission_classes = [IsAdminUser]

    queryset = QuestionnaireResult.objects.all()
    serializer_class = AdminResultSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        questionnaire = get_object_or_404(Questionnaire, pk=self.kwargs['questionnaire_pk'])
        questionnaire_content = QuestionnaireContent.objects.filter(questionnaire=questionnaire)
        return QuestionnaireResult.objects.filter(questionnaire_content__in=questionnaire_content, user=user)


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
