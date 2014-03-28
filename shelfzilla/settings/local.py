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
)

# Filer
FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'django.core.files.storage.FileSystemStorage',
            'OPTIONS': {},
            'UPLOAD_TO': 'shelfzilla.utils.filer_generate_randomized',
            'UPLOAD_TO_PREFIX': 'filer_public',
        },
        'thumbnails': {
            'ENGINE': 'django.core.files.storage.FileSystemStorage',
            'OPTIONS': {},
            'THUMBNAIL_OPTIONS': {
                'base_dir': 'filer_public_thumbnails',
            },
        },
    },
    'private': {
        'main': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(os.path.join(MEDIA_ROOT, '../smedia/filer_private')),
                'base_url': '/smedia/filer_private/',
            },
            'UPLOAD_TO': 'shelfzilla.utils.filer_generate_randomized',
            'UPLOAD_TO_PREFIX': '',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(os.path.join(MEDIA_ROOT, '../smedia/filer_private_thumbnails')),
                'base_url': '/smedia/filer_private_thumbnails/',
            },
            'THUMBNAIL_OPTIONS': {},
        },
    },
}
