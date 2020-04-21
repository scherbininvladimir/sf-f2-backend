from backend.views import QuestionList, QuestionDetail, QuestionnaireList, QuestionnaireDetail
from django.urls import path  

app_name = 'backend'  
urlpatterns = [  
    path('questions/', QuestionList.as_view(), name='question-list'),  
    path('questions/<int:pk>', QuestionDetail.as_view(), name='question-detail'),
    path('questionnaires/', QuestionnaireList.as_view(), name='questionnaires-list'),  
    path('questionnaires/<int:pk>', QuestionnaireDetail.as_view(), name='questionnaire-detail'), 
]