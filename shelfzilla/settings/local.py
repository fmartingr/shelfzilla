import dj_database_url
from .base import *


DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': dj_database_url.parse('postgres:///shelfzilla')
}
