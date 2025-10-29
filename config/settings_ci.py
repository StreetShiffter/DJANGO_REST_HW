from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# Переопределяем базу на SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Отключаем статику, если не нужна
STATICFILES_DIRS = []

# Обязательно: SECRET_KEY должен быть задан
SECRET_KEY = 'ci-test-secret-key-unsafe-but-ok'

DEBUG = True

# Отключаем email-бэкенд, если не нужен
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
