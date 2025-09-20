#  DJANGO REST Framework 

# 🔖 Описание проекта:

Данный проект является сервисом передачи данных по API из DJANGO REST FRAMEWORK.

# 🔧 Установка компонентов:


1. Создайте проект и установите poetry:


```pip install --user poetry```


2. Установите инструменты для реализации сервиса:

![Python](https://img.shields.io/badge/Python-3.13-green?logo=python&logoColor=white)

[![Django](https://img.shields.io/badge/Django-3.2.0-%2311677A?logo=django&logoColor=white&style=flat&labelColor=black)]( https://www.djangoproject.com/ )
![Django REST Framework](https://img.shields.io/badge/DJANGO-REST_FRAMEWORK-ff69b4?style=for-the-badge&logo=django&logoColor=white)
[![django-filter](https://img.shields.io/badge/django--filter-4.0.0-blue?logo=django&logoColor=white&style=for-the-badge)](https://django-filter.readthedocs.io/)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-black?logo=envoy&logoColor=orange)]( https://pypi.org/project/python-dotenv/ )
[![psycopg2](https://img.shields.io/badge/psycopg2-%233178C6?logo=postgresql&logoColor=white)]( https://pypi.org/project/psycopg2/ )
[![Pillow](https://img.shields.io/badge/Pillow-%23FF6B6B?logo=python&logoColor=white&style=flat&labelColor=black)]( https://pypi.org/project/Pillow/ )
[![IPython](https://img.shields.io/badge/IPython-%23779ECB?logo=ipython&logoColor=white&style=flat&labelColor=black)]( https://pypi.org/project/ipython/ )

![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-cache-8a2be2?logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge&logo=postgresql&logoColor=white)

![Black](https://img.shields.io/badge/black-000000?style=flat&logo=python&logoColor=white)
![Mypy](https://img.shields.io/badge/mypy-checked-blue.svg?logo=python&logoColor=green)
![Flake8](https://img.shields.io/badge/flake8-checked-blue.svg?logo=python&logoColor=blue)
![JSON](https://img.shields.io/badge/json-5E5C5C?logo=json&logoColor=red)

КОМАНДЫ ДЛЯ ЗАПУСКА ФРЕЙМВОРКА И ПРИЛОЖЕНИЯ
```
poetry add django # Установка django
poetry add djangorestframework # Установка django rest framework
poetry add django-filter # Установка фильтратора DRF
poetry add pillow # Установка библиотеки для работы с изображениями
poetry add dotenv # Установка библиотеки для работы с чувствительными данными
poetry add ipython # Установка библиотеки для работы с чувствительными данными
poetry add psycopg2 # Установка инструмента для работы с ORM

poetry add --dev flake8 mypy isort black # Eстановка всех dev зависимостей 

django-admin startproject config . # Старт нового проекта
django-admin startproject myproject # Старт нового приложения

python manage.py createsuperuser # дать суперпользователя для админки.
При выполнении этой команды необходимо указать имя пользователя и пароль.
Адрес электронной почты является опциональным параметром.

python manage.py shell -i ipython #Запуск DJANGO SHELL

```
🔄 ОБНОВЛЕНИЕ ДАННЫХ

ВНИМАНИЕ!!!
При создании фикстур для моделей использующие AbstractUser или AbstractBaseUser - фикстура создается
с нужными полями так же как из БД КРОМЕ ПОЛЕЙ:

-которые имеют null-true - не обязательно заполнять
-id-pk - не надо
-last_login - категорически нельзя

При записи через фикстуру обычных моделей — указываем все поля, кроме pk/id,
и тех, которые необязательны (null=True, blank=True)

Команда записи фикстуры:

python manage.py loaddata НАЗВАНИЕ_ФИКСТУРЫ.json --ignorenonexistent(игнорирование несуществующих связей)


# ✒️ Использование API
*Get запросы на список*
![Get запросы на список](./media/get.jpg)

*Get запросы на конкретный объект*
![Get запросы на конкретный объект](./media/get_pk.jpg)

Для POSTMAN можно выполнять фильтрацию и поиск, если они указаны в полях вьюшки-ендпоинте:
```
http://localhost:8000/users/payment/ - основа
http://localhost:8000/users/payment/?ordering=payment_date=false - сортировка по убыванию(указываем функцию и по какому полю из вьюшки)
http://localhost:8000/users/payment/?payment_method=transfer - фильтрация (можно не указывать поле filterset) 
```
![Get запросы на конкретный объект](./media/endpoint_filter_ordering.jpg)
```
️ ВАЖНО ⚠️
```
python manage.py runserver 8080 # Запуск сервера
CTRL+С # Отключение сервера
```
### 🌐 Пример страниц:
*Главная страница*
![Главная страница](./static/mailservices/images/home.jpg)


📡 API Документация
API доступно по адресу: http://localhost:8000/api/

Postman коллекция
Для удобства тестирования API предоставлена коллекция Postman:

📥 Скачать Postman Collection

Или импортируйте по ссылке (если опубликовано в Postman Cloud):

🔗 Открыть в Postman

💡 Совет: Импортируйте коллекцию в Postman → "Import" → "Link" или "File". 

📄 Лицензия
Этот проект лицензирован по MIT License — подробнее см. файл LICENSE.