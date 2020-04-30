from backend.views import (
    QuestionList, 
    QuestionDetail, 
    QuestionnaireList, 
    QuestionnaireDetail,
    ResultDetail,
    ResultCreate,
    UserList
)
from django.urls import path  

app_name = 'backend'  
urlpatterns = [  
    path('questions/', QuestionList.as_view(), name='question-list'),  
    path('questions/<int:pk>', QuestionDetail.as_view(), name='question-detail'),
    path('questionnaires/', QuestionnaireList.as_view(), name='questionnaires-list'),  
    path('questionnaires/<int:pk>', QuestionnaireDetail.as_view(), name='questionnaire-detail'), 
    path('result/create/', ResultCreate.as_view(), name='questionnaire-results'),
    path('result/get/<int:questionnaire_content_pk>', ResultDetail.as_view(), name='result-get'),
    path('result/update/<int:questionnaire_content_pk>', ResultDetail.as_view(), name='result-get'),
    

    # path('results_user/<int:user_pk>', QuestionnaireUserResultList.as_view(), name='questionnaire-results-for-user'),
    # path('result/<int:user_pk>/<int:questionnaire_content_pk>', ResultDetail.as_view(), name='questionnaire-result'),
    # path('users', UserList.as_view(), name='users'),
]