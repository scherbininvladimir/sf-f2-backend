from backend.views import (
    QuestionnaireList, 
    QuestionnaireContentList,
    ResultDetail,
    ResultCreate,
    Statistics,
    StatisticsDetail,
)
from django.urls import path  

app_name = 'backend'  
urlpatterns = [
    path('questionnaires/', QuestionnaireList.as_view(), name='questionnaires-list'),  
    path('questionnaires/<int:pk>', QuestionnaireContentList.as_view(), name='questionnaire-detail'), 
    path('result/create/', ResultCreate.as_view(), name='result-create'),
    path('result/get/<int:questionnaire_content_pk>', ResultDetail.as_view(), name='result-get'),
    path('result/update/<int:questionnaire_content_pk>', ResultDetail.as_view(), name='result-update'),
    path('admin/stat/', Statistics.as_view(), name='statistics'),
    path('admin/stat/<int:user_pk>/<int:questionnaire_pk>', StatisticsDetail.as_view(), name='statistics'),
]