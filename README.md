# sf-f2-backend

## Установка:
```
docker-compose up -d
```
## Использование:
```
GET /bboard/adverts/<advert_id> - получить объявление
GET /bboard/adverts/stat/<advert_id> - получить статистику объявления
POST /bboard/adverts - создать новый документ
PUT /bboar/adverts/<advert_id> - добавление комментариев и тегов


GET api/questionnaires/ - получение списка назначенных для пользователя опросников
GET api/ questionnaires/<int:pk> - получение данных для построения формы опросника
api/result/create/ - создание записи результата в базе данных (одновременно, в случае ограничения по времени, создается запись в redis с соответствующим таймаутом)
api/result/update/<int:questionnaire_content_pk> - обновление записи с результатом
api/admin/stat/ [name='statistics'] - общие данные (опросники, общие резульаты для каждого пользователя по каждому опросу)
api/admin/stat/<int:user_pk>/<int:questionnaire_pk> - ответы пользователя на вопросы
api/admin/questions/ - список вопросов для редактора вопросов
api/admin/questions/<int:pk> - создание и редактирование вопросов
api/admin/question_image/<filename>/<int:question_id> - добавление изображения к вопросу
api/admin/questionnaires/ Получение списка всех опросников для редактора опросников
api/admin/questionnaires/<int:pk> - создание и обновление опросника
api/token/ [name='token_obtain_pair'] - авторизация
api/refresh/ [name='token_refresh'] - обновление token
api/verify/ [name='token_verify'] - проверка авторизации


```
