from backend.views import (
    QuestionnaireList, 
    QuestionnaireContentList,
    ResultDetail,
    ResultCreate,
    AdminQuestionList,
    AdminQuestionDetail,
    PictureUploadView,
    AdminQuestionnaireList,
    AdminQuestionnaireDetail,
    AdminResults,
    AdminResultDetail,
)
from django.urls import path  

app_name = 'backend'  
urlpatterns = [
    path('questionnaires/', QuestionnaireList.as_view(), name='questionnaire-list'),  
    path('questionnaires/<int:pk>', QuestionnaireContentList.as_view(), name='questionnaire-detail'), 
    path('result/create/', ResultCreate.as_view(), name='result-create'),
    path('result/get/<int:questionnaire_content_pk>', ResultDetail.as_view(), name='result-get'),
    path('result/update/<int:questionnaire_content_pk>', ResultDetail.as_view(), name='result-update'),
    path('admin/stat/', AdminResults.as_view(), name='statistics'),
    path('admin/stat/<int:user_pk>/<int:questionnaire_pk>', AdminResultDetail.as_view(), name='statistics'),
    path('admin/questions/', AdminQuestionList.as_view(), name='admin-questions'),
    path('admin/questions/<int:pk>', AdminQuestionDetail.as_view(), name='admin-question'),
    path('admin/question_image/<filename>/<int:question_id>', PictureUploadView.as_view(), name='admin-question-image'),
    path('admin/questionnaires/', AdminQuestionnaireList.as_view(), name='admin-questionnaire-list'),
    path('admin/questionnaires/<int:pk>', AdminQuestionnaireDetail.as_view(), name='admin-questionnaire-detail'),
]