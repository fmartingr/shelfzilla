import os
import sys
import dj_database_url
import toml
from .base import *


this_module = sys.modules[__name__]

# Read configfile
with open(os.environ['APP_CONFIGFILE']) as conffile:
    config = toml.loads(conffile.read())

# Installed Apps
INSTALLED_APPS += tuple(config['global']['installed_apps'])

# Middleware classes
if 'middleware_classes' in config['global']:
    if 'prepend' in config['global']['middleware_classes']:
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + tuple(
            config['global']['middleware_classes']['prepend']
        )
    if 'append' in config['global']['middleware_classes']:
        MIDDLEWARE_CLASSES += tuple(
            config['global']['middleware_classes']['append']
        )

# Database
DATABASES = {
    'default': dj_database_url.parse(config['global']['database_url'])
}

# Overwrite values
for key, value in config['overwrite'].iteritems():
    setattr(this_module, key.upper(), value)

# Filer
FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'django.core.files.storage.FileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(
                    os.path.join(MEDIA_ROOT, 'filer/public/')),
                'base_url': '{}files/'.format(config['filer']['base_url']),
            },
            'UPLOAD_TO': 'shelfzilla.utils.filer_generate_randomized',
            'UPLOAD_TO_PREFIX': '',
        },
        'thumbnails': {
            'ENGINE': 'django.core.files.storage.FileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(
                    os.path.join(MEDIA_ROOT, 'filer/public/')),
                'base_url': '{}files/'.format(config['filer']['base_url']),
            },
            'THUMBNAIL_OPTIONS': {
                'base_dir': 'thumbnails',
            },
            'UPLOAD_TO_PREFIX': '',
        },
    },
    'private': {
        'main': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(
                    os.path.join(MEDIA_ROOT, 'filer/private')),
                'base_url': '/smedia/private/',
            },
            'UPLOAD_TO': 'shelfzilla.utils.filer_generate_randomized',
            'UPLOAD_TO_PREFIX': '',
        },
        'thumbnails': {
            'ENGINE': 'filer.storage.PrivateFileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(
                    os.path.join(MEDIA_ROOT, 'filer/private_thumbnails')),
                'base_url': '/smedia/private_thumbnails/',
            },
            'THUMBNAIL_OPTIONS': {},
        },
    },
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': config['log']['logfile'],
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
