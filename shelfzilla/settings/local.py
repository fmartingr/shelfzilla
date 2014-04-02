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

# Filer
STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'django.core.files.storage.FileSystemStorage',
            'OPTIONS': {},
            'UPLOAD_TO': 'shelfzilla.utils.generate_randomized',
            'UPLOAD_TO_PREFIX': 'public',
        },
        'thumbnails': {
            'ENGINE': 'django.core.files.storage.FileSystemStorage',
            'OPTIONS': {},
            'THUMBNAIL_OPTIONS': {
                'base_dir': 'public_thumbnails',
            },
        },
    },
    'private': {
        'main': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(os.path.join(MEDIA_ROOT, '../smedia/private')),
                'base_url': '/smedia/private/',
            },
            'UPLOAD_TO': 'shelfzilla.utils.generate_randomized',
            'UPLOAD_TO_PREFIX': '',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(os.path.join(MEDIA_ROOT, '../smedia/private_thumbnails')),
                'base_url': '/smedia/private_thumbnails/',
            },
            'THUMBNAIL_OPTIONS': {},
        },
    },
}
