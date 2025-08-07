# backend/app/settings.py
import os
from pathlib import Path
import logging.config
import dj_database_url

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-gw^4gif(3_2ijvc)l)ty0s-1e#2chgt@li=!+cnk#x&01nc*a)')
DEBUG = os.environ.get('DJANGO_ENV') != 'PRODUCTION'  # False in production
ALLOWED_HOSTS = ['chatgpt-backend-wbu0.onrender.com', 'localhost', '127.0.0.1']

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 自定义模板目录
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

# Logging
if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    os.makedirs(os.path.join(BASE_DIR, 'logs'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s [%(module)s|%(lineno)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {'level': 'INFO', 'class': 'logging.StreamHandler', 'formatter': 'simple'},
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filename': os.path.join(BASE_DIR, 'logs/default.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
        },
        'errors': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filename': os.path.join(BASE_DIR, 'logs/errors.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'errors'],
            'propagate': False,
            'level': 'INFO',
        },
        'default': {
            'handlers': ['console', 'default', 'errors'],
            'level': 'INFO',
        },
    },
}

logging.config.dictConfig(LOGGING)

# Application definition
INSTALLED_APPS = [
    'simpleui',  # 添加 simpleui，必须在 django.contrib.admin 之前
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'app.accounts',
    'app.chatgpt',
    'django_crontab',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS configuration
CORS_ALLOWED_ORIGINS = [
    'https://xy33.netlify.app',
    'http://localhost:5173',
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
]

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'
AUTH_USER_MODEL = 'accounts.User'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://chatgpt_mirror_db_user:d45mDxg2485RFNYab8UQOdRVLNu6MW4t@dpg-d29khp7gi27c73cn1ufg-a/chatgpt_mirror_db',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Custom 404 handler
handler404 = 'app.views.custom_404'

# Internationalization
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Environment-specific settings
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'LOCAL')
if DJANGO_ENV == 'PRODUCTION':
    print('PRODUCTION environment')
    try:
        from app.config.production import *
    except ImportError:
        pass
else:
    print('local environment')
    try:
        from app.config.local import *
    except ImportError:
        pass