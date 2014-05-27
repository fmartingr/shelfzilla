import os
import dj_database_url
from .base import *


DEBUG = True
TEMPLATE_DEBUG = True

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
)

FILER_DUMP_PAYLOAD = True


MEDIA_URL = '/media/'
STATIC_URL = '/static/'
