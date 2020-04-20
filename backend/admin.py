from django.contrib import admin
from .models import Question, Questionnaire, Questionnaire_content


class Questionnaire_contentInline(admin.TabularInline):
    model = Questionnaire_content

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = (Questionnaire_contentInline, )



