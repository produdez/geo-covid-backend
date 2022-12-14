"""
Django settings for geo_covid project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

import environ

# Default environment values
DEFAULT_DB_URL = 'mongodb://localhost:27017/'
env = environ.Env(
    # set casting, default value
    DEPLOY_ENV=(str,'dev'),
    DEBUG=(bool, True),
    SECRET_KEY=(str,'django-insecure-3!-(=vu^&v0pp*w*o)&5$3(4wu#jm(7!w1y=!*61@93#h94_d$'),
    DB_USERNAME=(str,'admin'),
    DB_PASSWORD=(str,'admin'),
    DB_URL=(str,'localhost'),
    DB_URL_TEST=(str,DEFAULT_DB_URL),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# ! Important variables
DEPLOY_ENV = env('DEPLOY_ENV')
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
DB_USERNAME = env('DB_USERNAME')
DB_PASSWORD = env('DB_PASSWORD')
DB_URL = env('DB_URL')


DB_URL_TEST = env('DB_URL_TEST') if DEPLOY_ENV == 'production' else DEFAULT_DB_URL
try:
    from pymongo import MongoClient
    client = MongoClient(
        host=DB_URL_TEST
    )
    db = client['geo-covid']
    print('Db collection list: ',db.list_collection_names())
except Exception as e:
    print('exception: ', e)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # app
    'us_covid_api', 
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # django_rest_api
    'rest_framework',
    # extension
    'django_extensions',
    # api doc ui
    'drf_spectacular',
    'drf_spectacular_sidecar',
    # cors
    "corsheaders",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # cors
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = 'geo_covid.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'geo_covid.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

client = {
    'host': DB_URL,
    'username' : DB_USERNAME,
    'password' : DB_PASSWORD,
} if DEPLOY_ENV == 'production' else {
    'host': 'localhost'
}
print('client: ', client)
# from requests import get

# ip = get('https://api.ipify.org').content.decode('utf8')
# print('My public IP address is: {}'.format(ip))
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'geo-covid',
        'ENFORCE_SCHEMA': True,
        'CLIENT': client,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATIC_DIRS = [
     os.path.join(BASE_DIR, 'static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Settings for django_api
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', # needed settings for drf_spectacular
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 400 # We have 56 states so 60 will make it so that all our state data returns in one request
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Geo Covid API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True # NOTE: remove this when want to restrict backend access
