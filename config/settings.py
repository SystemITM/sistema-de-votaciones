import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,web").split(",")
INSTALLED_APPS = ["django.contrib.contenttypes", "django.contrib.auth", "rest_framework", "drf_spectacular", "voting"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "django.middleware.common.CommonMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql", "NAME": os.getenv("POSTGRES_DB", "voting"), "USER": os.getenv("POSTGRES_USER", "voting"), "PASSWORD": os.getenv("POSTGRES_PASSWORD", "voting"), "HOST": os.getenv("DB_HOST", "db"), "PORT": os.getenv("DB_PORT", "5432")}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REST_FRAMEWORK = {"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema", "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"]}
SPECTACULAR_SETTINGS = {"TITLE": "Sistema de Votaciones API", "VERSION": "1.0.0"}
