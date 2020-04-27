from datetime import datetime

from django.db import models
from django.contrib.auth.models import User  

from django.contrib.postgres.fields import JSONField

QUESTION_TYPE = [
    ('T', 'Тест'),
    ('Q', 'Опрос'),
]

class Question(models.Model):
    title = models.CharField("Название вопроса", max_length=128)
    content = models.CharField("Содержание вопроса", max_length=255)
    question_type = models.CharField("Тип вопроса", max_length=2, choices=QUESTION_TYPE, default='Тест')
    response_options = JSONField("Ответы", default=list)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Questionnaire(models.Model):
    title = models.CharField("Название опросника", max_length=128)
    start_date = models.DateField("Дата начала опроса", default=datetime.now, blank=False)
    end_date = models.DateField("Дата окончания опроса", default=datetime.now, blank=False)
    description = models.TextField(blank=True, null=True)
    questions = models.ManyToManyField(
        Question,
        through="QuestionnaireContent"
    )
    target_users = models.ManyToManyField(
        User, verbose_name="Сотрудники"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Опросник"
        verbose_name_plural = "Опросники"


class QuestionnaireContent(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, verbose_name="Опросник")
    time_to_answer = models.SmallIntegerField("Время на ответ")
    answer_weight = models.SmallIntegerField("Вес ответа")

    def __str__(self):
        return f"{self.questionnaire} - {self.question} - {self.time_to_answer} - {self.answer_weight}"

    class Meta:
        verbose_name = "Содержимое опросника"
        verbose_name_plural = "Содержимое опросников"

class QuestionnaireResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Сотрудник")
    questionnaire_content = models.ForeignKey(QuestionnaireContent, on_delete=models.PROTECT)
    result = models.SmallIntegerField()

    class Meta:
        verbose_name = "Результат по опроснику"
        verbose_name_plural = "Результаты по всем опросникам"