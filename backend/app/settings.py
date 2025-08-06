import os
from pathlib import Path
import logging.config

# Build paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-gw^4gif(3_2ijvc)l)ty0s-1e#2chgt@li=!+cnk#x&01nc*a)")
DEBUG = os.environ.get("DJANGO_ENV") != "PRODUCTION"  # 生产环境中 DEBUG = False
ALLOWED_HOSTS = ["chatgpt-backend-wbu0.onrender.com", "localhost", "127.0.0.1"]

# Logging
if not os.path.exists(os.path.join(BASE_DIR, "logs")):
    os.makedirs(os.path.join(BASE_DIR, "logs"))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] %(levelname)s [%(module)s|%(lineno)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "simple"},
        "default": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "simple",
            "filename": os.path.join(BASE_DIR, "logs/default.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
        },
        "errors": {
            "level": "WARNING",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "simple",
            "filename": os.path.join(BASE_DIR, "logs/errors.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "errors"],
            "propagate": False,
            "level": "INFO",
        },
        "default": {
            "handlers": ["console", "default", "errors"],
            "level": "INFO",
        },
    },
}

logging.config.dictConfig(LOGGING)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "app.accounts",
    "app.chatgpt",
    "django_crontab",
    "corsheaders",  # 添加 django-cors-headers
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # 添加，放在最前面
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS 配置
CORS_ALLOWED_ORIGINS = [
    "https://xy33.netlify.app",  # 前端域名
    "http://localhost:5173",     # 本地开发
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
]

REST_FRAMEWORK = {
    "PAGE_SIZE": 10,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}

ROOT_URLCONF = "app.urls"
WSGI_APPLICATION = "app.wsgi.application"
AUTH_USER_MODEL = "accounts.User"

# Database
DB_PATH = os.path.join(BASE_DIR, "db")
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(DB_PATH, "db.sqlite3"),
    }
}

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Custom 404 handler
handler404 = "app.views.custom_404"

# Internationalization
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Environment-specific settings
DJANGO_ENV = os.environ.get("DJANGO_ENV", "LOCAL")
if DJANGO_ENV == "PRODUCTION":
    print("PRODUCTION environment")
    try:
        from app.config.production import *
    except ImportError:
        pass
else:
    print("local environment")
    try:
        from app.config.local import *
    except ImportError:
        pass