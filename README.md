
#  YAMDB - API для хранения отзывов на произведения искусства


## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```BASH
git clone git@github.com/brava05/api_yamdb
```
Cоздать и активировать виртуальное окружение:
```BASH
python -m venv env
source env/venv/activate
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```BASH
pip install -r requirements.txt
```
Выполнить миграции:
```BASH
python3 manage.py migrate
```
Запустить проект:
```BASH
python3 manage.py runserver
```
## Авторизация:

1. Отправляем POST запрос на адрес
http://127.0.0.1:8000/api/v1/auth/signup/

В теле пишем имя пользователя, которого хотим создать, 
и почту, на которую получим код подтверждения.
```JSON
{
    "username": "admin6",
    "email": "brava_05@mail.ru"
}
```

Получаем на почту письмо с кодом подтверждения. К примеру
confirmation_code = "OHC8U9fgUtDa6ttpzD6EGvT689jS9cjC"

Теперь осталось только получить токен, для доступа к API

2. Отправляем POST запрос на адрес
http://127.0.0.1:8000/api/v1/auth/token/

в теле указываем того же пользователя и код подтверждения из письма
```JSON
{
    "username": "admin6",
    "confirmation_code": "OHC8U9fgUtDa6ttpzD6EGvT689jS9cjC"
}
```
Получаем в ответ токен, которые используем для автороизации в дальнейшей работе
```JSON
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYyMDQzODkwLCJpYXQiOjE2NjIwMTM4OTAsImp0aSI6IjViZWI3ZDg4YTg5MDQxZmVhY2RlOWM2YTUzOTMyYTQ4IiwidXNlcl9pZCI6MTA1fQ.II1QHxuSysvSkPilhbYw4Pi-I7MpD-q_M1Uzt-e0aT0"
}
```

## Получение данных:
Данные можно получить, отправив GET запрос к таким поинтам
http://127.0.0.1:8000/api/v1/categories/ - список категорий
http://127.0.0.1:8000/api/v1/genres/ - список жанров
http://127.0.0.1:8000/api/v1/titles/ - список произведений

Отзывы можно получить только для определенного произведения
Адрес должен быть такой формы
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
где title_id - это ид номер конкретного произведения.

Комментарии доступны только при указании произведения и конкретного отзыва к нему
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
где title_id - это ид номер конкретного произведения
а review_id - ид номер отзыва.

## Добавление данных:
Добавить отзыв можно отправив POST-запрос на адрес
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
где title_id - это ид номер конкретного произведения

В теле запроса должен быть JSON такого формата
```JSON
{
"text": "string",
"score": 1
}
```
где text - это текст самого отзыва
score - ваша оценка произведения.

Добавить комментарий можно отправив POST-запрос на адрес
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
где title_id - это ид номер конкретного произведения
а review_id - ид номер отзыва.

В теле запроса должен быть JSON такого формата
```JSON
{
"text": "string"
}
```
где text - это текст комментария.

Авторы: Бражинский Валерий, Глотов Руслан, Марханов Александр
