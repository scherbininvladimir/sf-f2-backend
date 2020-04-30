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


class QuestionDetail(generics.RetrieveUpdateAPIView):  
    
    queryset = Question.objects.all()  
    serializer_class = QuestionSerializer


class QuestionnaireList(generics.ListAPIView):

    serializer_class = QuestionnaireSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return get_list_or_404(Questionnaire)
        else:
            return get_list_or_404(Questionnaire, target_users=self.request.user)


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
        return get_object_or_404(QuestionnaireResult, questionnaire_content=questionnaire_content, user=self.request.user)


class ResultCreate(generics.CreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = QuestionnaireRusultSerilizer




# class QuestionnaireResultList(generics.ListCreateAPIView):
    
#     serializer_class = QuestionnaireRusultSerilizer

#     def get_queryset(self):
#         questionnaire = get_object_or_404(Questionnaire, pk=self.kwargs['questionnaire_pk'])
#         questionnaire_contents = QuestionnaireContent.objects.filter(questionnaire=questionnaire)
#         return QuestionnaireResult.objects.filter(questionnaire_content__in=questionnaire_contents)       
    

# class QuestionnaireUserResultList(generics.ListCreateAPIView):
    
#     serializer_class = QuestionnaireRusultSerilizer
    
#     def get_queryset(self):
#         user = get_object_or_404(User, id=self.kwargs['user_pk'])
#         return QuestionnaireResult.objects.filter(user=user)
    
#     def has_permission(self, request, view):
#         if request.user.is_staff:
#             return True
#         else:
#             if self.kwargs['user_pk'] == request.user.pk:
#                 return True
#         return False
