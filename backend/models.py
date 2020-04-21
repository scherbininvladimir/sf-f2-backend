from django.db import models
from django.contrib.auth.models import User  


class Question(models.Model):
    name = models.CharField("Название вопроса", max_length=128)
    content = models.CharField("Содержание вопроса", max_length=255)
    image = models.ImageField("Изображение", upload_to='uploads/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Questionnaire(models.Model):
    name = models.CharField("Название опросника", max_length=128)
    # start_date = models.DateField("Дата начала опроса")
    time_to_live = models.SmallIntegerField("Срок сбора ответов в днях")
    questions = models.ManyToManyField(
        Question,
        through="Questionnaire_content"
    )
    target_users = models.ManyToManyField(
        User, verbose_name="Сотрудники"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Опросник"
        verbose_name_plural = "Опросники"


class Questionnaire_content(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, verbose_name="Опросник")
    time_to_answer = models.SmallIntegerField("Время на ответ")
    answer_weight = models.SmallIntegerField("Вес ответа")

    class Meta:
        verbose_name = "Содержимое опросника"
        verbose_name_plural = "Содержимое опросников"

class Questionnaire_ruslults(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Сотрудник")
    questionnaire_content = models.ForeignKey(Questionnaire_content, on_delete=models.PROTECT)
    rusult = models.SmallIntegerField()

    class Meta:
        verbose_name = "Результат по опроснику"
        verbose_name_plural = "Результаты по всем опросникам"