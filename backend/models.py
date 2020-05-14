from datetime import datetime
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User  
from django.utils import timezone

ANSWER_TYPE = [
    ('O', 'Один'),
    ('M', 'Много'),
]

QUESTION_TYPE = [
    ('Q', 'Опросник'),
    ('T', 'Тест'),
]

class Question(models.Model):
    title = models.CharField("Название вопроса", max_length=128)
    content = models.CharField("Содержание вопроса", max_length=255)
    picture = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    answers_number = models.CharField("Количество принимаемых ответов", max_length=2, choices=ANSWER_TYPE, default='O')
    question_type = models.CharField("Тип вопроса", max_length=2, choices=QUESTION_TYPE, default='T')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Response(models.Model):
    question = models.ForeignKey(Question, related_name='response', on_delete=models.CASCADE, verbose_name = "Вопрос")
    response_option = models.CharField("Ответ на вопрос", max_length=255)
    isCorrect = models.BooleanField("Верный ответ в тестовом вопросе", default=False)
    answer_weight = models.SmallIntegerField("Вес ответа в опроснике", default=0)  
    

class AnswerQuestionnaire(models.Model):
    question = models.ForeignKey(Question, related_name='questionnair_answer', on_delete=models.CASCADE)
    answer = models.CharField("Ответ на вопрос", max_length=255)
      

class Questionnaire(models.Model):
    title = models.CharField("Название опросника", max_length=128)
    start_date = models.DateField("Дата начала опроса", default=datetime.now, blank=True)
    end_date = models.DateField("Дата окончания опроса", default=datetime.now, blank=True)
    description = models.TextField(blank=True, null=True)
    allow_answer_modify = models.BooleanField("Разрешить пользователю менять сохраненные ответы", default=False)
    time_to_answer = models.SmallIntegerField("Время прохождения опроса", default=0)
    questions = models.ManyToManyField(
        Question,
        through="QuestionnaireContent"
    )
    target_users = models.ManyToManyField(
        User, verbose_name="Сотрудники"
    )
    
    @property
    def isOpen(self):
        if self.end_date >= datetime.today().date(): 
            return True
        else:
            return False
        
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Опросник"
        verbose_name_plural = "Опросники"


class QuestionnaireContent(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, verbose_name="Опросник")
    time_to_answer = models.SmallIntegerField("Время на ответ", default=0)
    answer_weight = models.SmallIntegerField("Вес ответа", default=1)

    def __str__(self):
        return f"{self.questionnaire} - {self.question} - {self.time_to_answer} - {self.answer_weight}"

    class Meta:
        verbose_name = "Содержимое опросника"
        verbose_name_plural = "Содержимое опросников"


class QuestionnaireResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Сотрудник")
    questionnaire_content = models.ForeignKey(QuestionnaireContent, on_delete=models.PROTECT)
    answer = JSONField(default=list)

    @property
    def score(self):
        question = self.questionnaire_content.question
        answerList = []
        if not isinstance (self.answer, list):
            answerList.append(self.answer)
        else:
            answerList = self.answer
        response = Response.objects.filter(question=question)
        answer_score = 0
        for i in response:
            if self.questionnaire_content.question.question_type == 'Q':
                for j in answerList:
                    if i.response_option == j:
                        answer_score += i.answer_weight
            if self.questionnaire_content.question.question_type == 'T':
                for j in answerList:
                    if i.response_option == j:
                        if i.isCorrect:
                            answer_score += 1
                        else:
                            answer_score -= 1
        return answer_score * self.questionnaire_content.answer_weight

    class Meta:
        verbose_name = "Результат по опроснику"
        verbose_name_plural = "Результаты по всем опросникам"