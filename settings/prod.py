from .base import *
import django_heroku
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["klantointerview.herokuapp.com"]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 500,
    }
}

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
STATIC_ROOT = [
    os.path.join(BASE_DIR, 'static'),
]


django_heroku.settings(locals())
