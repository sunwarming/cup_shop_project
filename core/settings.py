import os
from pathlib import Path
import dj_database_url
from decouple import config, Csv

# Инициализация базового каталога проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================================
# 1. ОСНОВНЫЕ НАСТРОЙКИ БЕЗОПАСНОСТИ И ОКРУЖЕНИЯ
# =====================================================================

# Читаем секретный ключ из .env (или переменных Railway). Если его нет — берем дефолтный
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-secret-key-cup-shop')

# Превращаем строковое значение "True"/"False" в реальный тип bool
DEBUG = config('DEBUG', default=False, cast=bool)

# Парсим разрешенные хосты из строки через запятую
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())

# Если мы залили проект на Railway (DEBUG отключен), автоматически добавляем домен платформы
if not DEBUG:
    ALLOWED_HOSTS.append('.up.railway.app')


# =====================================================================
# 2. ОПРЕДЕЛЕНИЕ ПРИЛОЖЕНИЙ (APPS)
# =====================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Сторонние библиотеки
    'rest_framework',
    
    # Твое приложение магазина кружек
    'shop',
]


# =====================================================================
# 3. МИДЛВАР (MIDDLEWARE)
# =====================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise должен стоять СРАЗУ после SecurityMiddleware для быстрой раздачи CSS/JS
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'


# =====================================================================
# 4. ШАБЛОНЫ (TEMPLATES)
# =====================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Поиск глобальной папки templates, если она есть в корне
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# =====================================================================
# 5. КОНФИГУРАЦИЯ БАЗЫ ДАННЫХ (SQLite / PostgreSQL)
# =====================================================================

# Автоматический парсинг переменной DATABASE_URL от Railway. 
# Если её нет в системе (локально), плавно откатываемся на db.sqlite3.
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}


# =====================================================================
# 6. ВАЛИДАЦИЯ ПАРОЛЕЙ
# =====================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =====================================================================
# 7. ИНТЕРНАЦИОНАЛИЗАЦИЯ (ЯЗЫК И ВРЕМЯ)
# =====================================================================

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_TZ = True


# =====================================================================
# 8. СТАТИЧЕСКИЕ ФАЙЛЫ И МЕДИА (WhiteNoise Сборка)
# =====================================================================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Настройки для загружаемых картинок кружек
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Хранилище статики: включает сжатие файлов gzip/brotli и уникальное кеширование
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# =====================================================================
# 9. НАСТРОЙКИ DJANGO REST FRAMEWORK (DRF)
# =====================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    # По умолчанию для всего проекта требуем авторизацию, 
    # а в ProductViewSet мы переопределили её на IsAdminOrReadOnly
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


# =====================================================================
# 10. ПРАВИЛА БЕЗОПАСНОСТИ ДЛЯ ПРОДАКШНА (DEBUG = False)
# =====================================================================

if not DEBUG:
    # Защита куки сессий и CSRF-токенов (передача только по HTTPS)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # Доверяем домену Railway для отправки форм и PATCH/POST запросов
    CSRF_TRUSTED_ORIGINS = ['https://*.up.railway.app']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'