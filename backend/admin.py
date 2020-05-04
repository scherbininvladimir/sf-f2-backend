from django.contrib import admin
from django import forms

from .models import Question, Response, Questionnaire, QuestionnaireContent


class ResponseTInline(admin.TabularInline):
    model = Response


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = (ResponseTInline, )

    def has_module_permission(self, request):
        return True
    
    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class QuestionnaireContentInline(admin.TabularInline):
    model = QuestionnaireContent


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = (QuestionnaireContentInline, )

    def has_module_permission(self, request):
        return True
    
    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
