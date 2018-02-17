"""
Django settings for cadizm project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import socket
import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'var', 'log'))

secrets = yaml.load(open(os.path.join(BASE_DIR, 'secrets.yml')).read())

SECRET_KEY = secrets['DJANGO_SECRET_KEY']

GOOGLE_API_KEY = secrets['GOOGLE_API_KEY']

FCKCO_CLIENT_ID = secrets['FCKCO_CLIENT_ID']
FCKCO_CLIENT_SECRET = secrets['FCKCO_CLIENT_SECRET']

DEBUG = False

# SECURITY WARNING: don't run with debug turned on in production!
if socket.gethostname() in ['l00k', ]:
    DEBUG = True

HOST_NAME = 'cadizm.com'

ALLOWED_HOSTS = ['192.168.101.3', '.cadizm.com']
if DEBUG:
    ALLOWED_HOSTS.append('localhost')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'cadizm.bookmarks',
    'cadizm.theta360',
    'cadizm.about',
    'cadizm.instagram',
    'cadizm.tees',
    'cadizm.headspace',
]

if DEBUG:
    INSTALLED_APPS.append('django_extensions')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cadizm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

WSGI_APPLICATION = 'cadizm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'cadizm',
        'USER': 'cadizm',
        'PASSWORD': secrets['POSTGRES_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'cadizm', 'static'),
]

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(module)s %(funcName)s %(lineno)s %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'cadizm-debug.log'),
            'formatter': 'simple',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'cadizm-error.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cadizm': {
            'handlers': ['console', 'file_debug', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


CADIZM_STRIPE_PUB_KEY = secrets['CADIZM_STRIPE_LIVE_PUB_KEY']
CADIZM_STRIPE_SECRET_KEY = secrets['CADIZM_STRIPE_LIVE_SECRET_KEY']

if DEBUG:
    CADIZM_STRIPE_PUB_KEY = secrets['CADIZM_STRIPE_TEST_PUB_KEY']
    CADIZM_STRIPE_SECRET_KEY = secrets['CADIZM_STRIPE_TEST_SECRET_KEY']


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = secrets['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = secrets['EMAIL_HOST_PASSWORD']
EMAIL_USE_LOCALTIME = True

ROYS_SLACK_ACCESS_TOKEN = secrets['ROYS_SLACK_ACCESS_TOKEN']
