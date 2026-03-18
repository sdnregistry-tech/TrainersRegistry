"""
Django settings for TrainerRegistry_site project.

Modified to support PyInstaller packaging.
"""

import sys
import os
from pathlib import Path
from celery.schedules import crontab

# ---------------------------
# Base directory
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# PyInstaller support
# ---------------------------
if getattr(sys, 'frozen', False):
    # Running as PyInstaller exe
    BASE_DIR = Path(sys._MEIPASS)

# ---------------------------
# Quick-start development settings
# ---------------------------
SECRET_KEY = 'django-insecure-g2($b$74t5&sn0pyei91f@jr_qizfc0zxa1ru4vk1u6*8e2v18'
DEBUG = True
ALLOWED_HOSTS = []

# ---------------------------
# Installed apps
# ---------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'trainer',
    'widget_tweaks',
]

# ---------------------------
# Middleware
# ---------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------
# URL Configuration
# ---------------------------
ROOT_URLCONF = 'TrainerRegistry_site.urls'
WSGI_APPLICATION = 'TrainerRegistry_site.wsgi.application'

# ---------------------------
# Templates
# ---------------------------
TEMPLATES_DIR = BASE_DIR / 'TrainerRegistry_site' / 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ---------------------------
# Database
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------
# Password validators
# ---------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------
# Internationalization
# ---------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------
# Static files
# ---------------------------
STATIC_URL = 'static/'

if getattr(sys, 'frozen', False):
    # PyInstaller exe
    STATICFILES_DIRS = [BASE_DIR / 'TrainerRegistry_site' / 'static']
else:
    STATICFILES_DIRS = [BASE_DIR / 'static']

# ---------------------------
# Default primary key field type
# ---------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------
# Email configuration
# ---------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sdnregistry@gmail.com'
EMAIL_HOST_PASSWORD = 'sdn_registry2026'
DEFAULT_FROM_EMAIL = 'sdnregistry@gmail.com'

# ---------------------------
# Celery configuration
# ---------------------------
CELERY_BROKER_URL = 'redis://localhost:6379/0'

CELERY_BEAT_SCHEDULE = {
    'daily-expiration-check': {
        'task': 'yourapp.tasks.send_expiration_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
}