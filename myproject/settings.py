from pathlib import Path
from decouple import config
import dj_database_url
import logging
import os

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Logging
logging.basicConfig(level=logging.DEBUG)

# Static and media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Directory with your static files
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory to collect static files for deployment
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Secret key and debug mode
SECRET_KEY = config('SECRET_KEY', default='django-insecure-9ab2w4)bm8fw+lxjr=k4hm9+nvq7f*o8cf^2*f+7!l6ym7a=!3')
DEBUG = config('DEBUG', default=True, cast=bool)

# Allowed hosts and CSRF trusted origins
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com', 'http://127.0.0.1:8000']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',
    'users',
    'core'
]

# Add debug_toolbar only in debug mode
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Ensure static files are served
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",  # ✅ Ensure this includes the main templates folder
            BASE_DIR / "core" / "templates",  # ✅ Ensure Django checks core/templates
        ],
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

WSGI_APPLICATION = 'myproject.wsgi.application'

# Database configuration
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://event_management_db_vd2z_user:iPuFN2UgBOjBtSQMscKGfLoRwgLiNRgb@dpg-cub04qhopnds73efd9gg-a.oregon-postgres.render.com/event_management_db_vd2z',
        conn_max_age=600,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internal IPs for Debug Toolbar
if DEBUG:
    INTERNAL_IPS = [
        '127.0.0.1',  # Localhost
    ]
