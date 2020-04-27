from django.contrib import admin
from django import forms
from django_admin_json_editor import JSONEditorWidget

from .models import Question, Questionnaire, QuestionnaireContent


def dynamic_schema(widget):
    return {
        'type': 'array',
        'title': 'Варианты ответов',
        'items': {
            'title': "Вариант ответа",
            'type': 'object',
            'required': [
                'option',
                'is_correct',
            ],
            'properties': {
                'option': {
                    'title': 'Вариант ответа',
                    'type': 'string',
                    'format': 'text',
                    'minLength': 1,
                },
                'is_correct': {
                    'title': 'Верный ответ',
                    'type': 'boolean',
                }
             }
        }
    }

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        widget = JSONEditorWidget(dynamic_schema, False)
        form = super().get_form(request, obj, widgets={'response_options': widget}, **kwargs)
        return form

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
