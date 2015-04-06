import os
import dj_database_url
from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ('127.0.0.1', 'localhost')
INTERNAL_IPS = ('127.0.0.1', )

DATABASES = {
    'default': dj_database_url.parse('postgres:///shelfzilla')
}

# Bower
STATICFILES_DIRS += (
    os.path.join(BASE_DIR, "..", "static_components"),
)

# Apps
INSTALLED_APPS += (
    'django.contrib.webdesign',
    'rosetta',
    'django_extensions',
)

FILER_DUMP_PAYLOAD = True


MEDIA_URL = 'http://localhost:8000/media/'
STATIC_URL = 'http://localhost:8000/static/'

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-fdfc57f2bfb35a4ba5f9c1e3c30af373'
MAILGUN_SERVER_NAME = 'sandbox2dd21e486d144dc59742738b15e494ee.mailgun.org'
FROM_EMAIL = 'info@shelfzilla.com'
