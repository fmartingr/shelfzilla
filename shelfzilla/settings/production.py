import os
import dj_database_url
from .base import *


DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'default': dj_database_url.parse(os.environ['APP_DATABASE_URL'])
}

INSTALLED_APPS = (
    'gunicorn',
)

STATIC_ROOT = os.environ['APP_STATIC_ROOT']
STATIC_URL = os.environ['APP_STATIC_URL']

MEDIA_ROOT = os.environ['APP_MEDIA_ROOT']
MEDIA_URL = os.environ['APP_MEDIA_URL']

SECRET_KEY = os.environ['APP_SECRET_KEY']

INTERNAL_IPS = os.environ['APP_INTERNAL_IPS'].split(',')
ALLOWED_HOSTS = os.environ['APP_ALLOWED_HOSTS'].split(',')
