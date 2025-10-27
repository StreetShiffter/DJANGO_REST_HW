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

ПРОВЕРКА В DJANGO_SHELL на названия нужных прав:
```
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Найди контент-тип для модели Course
course_ct = ContentType.objects.get(app_label='educations', model='course')
lesson_ct = ContentType.objects.get(app_label='educations', model='lesson')

# Посмотри разрешения
perms = Permission.objects.filter(
    content_type__in=[course_ct, lesson_ct],
    codename__in=[
        'add_course', 'change_course',
        'add_lesson', 'change_lesson'
    ]
)

for p in perms:
    print(p.codename, p.id)
```


```
️ ВАЖНО ⚠️

python manage.py runserver 8080 # Запуск сервера
CTRL+С # Отключение сервера
```

🔝 РАБОТА с CELERY 
*Запуск команд воркера и планера*
```
poetry run celery -A config worker -l INFO -P eventlet
poetry run celery -A config beat -l INFO
poetry run celery -A my_project worker —loglevel=info
poetry run celery -A my_project beat —loglevel=info
```
Далее работа в *setting.py*
```
INSTALLED_APPS = [
    # ... другие приложения ...
    'django_celery_beat',
]
```
💡ВАЖНО💡
ВЫПОЛНИТЕ МИГРАЦИИ ДО РАБОТЫ С ПЛАНЕРОМ + запустите REDIS 
```
poetry run python manage.py migrate
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
### 📶 Работа с запросами
```
http://localhost:8000/users/payment/ - основа
http://localhost:8000/users/payment/?ordering=payment_date=false - сортировка по убыванию(указываем функцию и по какому полю из вьюшки)
http://localhost:8000/users/payment/?payment_method=transfer - фильтрация (можно не указывать поле filterset) 

Регистрация:
http://localhost:8000/users/register/ - post(json-raw)

Вход и получение токена post:
http://localhost:8000/users/login/ в body отправить json (json-raw)

Просмотр профиля get:
http://localhost:8000/users/profile/ (headers) Accept -Bearer  токен 

Редактирование профиля patch:
http://localhost:8000/users/profile/ (json-raw) patch + (headers) Accept -Bearer токен

Редактирование профиля полностью( нужны важные поля входа в аккаунт) put:
http://localhost:8000/users/profile/ (json-raw) patch + (headers) Accept - Bearer токен 

Удаление профиля delete:
http://localhost:8000/users/profile/delete (headers) Bearer  токен 

Просмотр списков пользователя get:
http://localhost:8000/users/list/(headers) Accept - Bearer  токен 

Отправка refresh токена post:
http://localhost:8000/users/list/(headers) Content-Type - application/json/ 
в body отправить json
{"refresh":"токен"} 
```

### DOCKER
ЭТАПЫ ЗАПУСКА КОНТЕЙНЕРОВ(при compose)
1.*Пишем Dockerfile*
2.*Пишем docker-compose.yml*
3.*Выполняем сборку: docker-compose build*
4.*Запускаем: docker-compose up -d*
    ИЛИ
  *Можно унифицировать: docker-compose up -d --build* -
    - Если образы для сервисов еще не созданы, они будут собраны перед запуском.

Команда для создания образа из докерфайла с присваиванием имени(-t)
(важно что бы poetry lock и toml использовали одну версию пайтона)
```
docker build -t django_rest_hw .
```

Команда просмотра образов
```
docker images
```
Команда просмотра логов

```
docker logs my-django-app
```
Команда просмотра контейнеров и удаления по id 
```
docker ps  
docker stop <контейнер id>
```

Команда остановки контейнера и чистки кэша
```
docker stop my-django-app
docker rm my-django-app
```

Запуск контейнера с параметрами .env как 1 контейнер на фоне(-d)
-указываем имя контейнера(--name)
-порт(-p)
-env-файл (--env-file)
- и имя образа
*(d settings ALLOWED_HOSTS = ['*'] для разработки)*
```
docker run -d --name my-django-app -p 8000:8000 --env-file .env django_rest_hw
```

Команда повторного запуска контейнера
```
docker start my-django-app
```

РАБОТА С DOCKER COMPOSE

Сборка образа на фоне(-d)
```
docker-compose up -d --build
```

Остановка всех работающих контейнеров
```
docker-compose down
```

Просмотр логов и id всех контейнеров
```
docker-compose logs
docker-compose ps
```

!!! ПРИМЕНЕНИЕ МИГРАЦИЙ НА СЕРВЕРЕ ТОЛЬКО ВРУЧНУЮ !!!
```
1 - ssh your_user@your_server_ip - вход на сервер
2 - cd /path/to/your/django-project/ - переходим в папку с проектом
3 - docker-compose ps - проверка запущеных контейнеров
4 - docker-compose exec web python manage.py migrate --noinput - миграции в терминале
# Важно ставить флаг --noinput  для игнорирования интерактивного ввода подтверждения
```
или через GitHub Actions

📄 Лицензия
Этот проект лицензирован по MIT License — подробнее см. файл LICENSE.