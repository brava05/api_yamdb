#  django project for API creation and testing



## Предоставляет удобный инструментарий:
для проверки навыков создания API и его тестирования


## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

git clone git@github.com:RuslGL/api_yatube.git

Cоздать и активировать виртуальное окружение:
python -m venv env
source env/venv/activate
python -m pip install --upgrade pip

Установить зависимости из файла requirements.txt:
pip install -r requirements.txt

Выполнить миграции:
python3 manage.py migrate

Запустить проект:
python3 manage.py runserver

## Примеры использования:

GET http://127.0.0.1:8000/api/v1/users/

RESPONSE:
