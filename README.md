# sf-f2-backend

## Установка:
```
docker-compose up
```
## Использование:
```
GET api/questionnaires/ - получение списка назначенных для пользователя опросников
GET api/ questionnaires/<int:pk> - получение данных для построения формы опросника
POST api/result/create/ - создание записи результата в базе данных (одновременно, в случае ограничения по времени, создается запись в redis с соответствующим таймаутом)
PUT api/result/update/<int:questionnaire_content_pk> - обновление записи с результатом
GET api/admin/stat/ [name='statistics'] - общие данные (опросники, общие резульаты для каждого пользователя по каждому опросу)
GET api/admin/stat/<int:user_pk>/<int:questionnaire_pk> - ответы пользователя на вопросы
GET api/admin/questions/ - список вопросов для редактора вопросов
POST, PUT api/admin/questions/<int:pk> - создание и редактирование вопросов
PUT api/admin/question_image/<filename>/<int:question_id> - добавление изображения к вопросу
GET api/admin/questionnaires/ Получение списка всех опросников для редактора опросников
POST, PUT api/admin/questionnaires/<int:pk> - создание и обновление опросника
POST api/token/ [name='token_obtain_pair'] - авторизация
POST api/refresh/ [name='token_refresh'] - обновление token
POST api/verify/ [name='token_verify'] - проверка авторизации


```
