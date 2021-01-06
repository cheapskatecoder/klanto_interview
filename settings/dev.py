from .base import *
import django_heroku

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'klanto',
        'USER': 'postgres',
        'PASSWORD': 'postgres'
    }
}

django_heroku.settings(locals())