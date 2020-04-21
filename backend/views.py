from .serializers import QuestionSerializer, QuestionnaireSerializer
from rest_framework import generics  

from .models import Question, Questionnaire

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
