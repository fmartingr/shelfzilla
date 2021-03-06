"""
Django settings for shelfzilla project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

_ = lambda x: x


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0123456789'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # Auth
    'django.contrib.auth',
    'shelfzilla.apps.account',

    # Admin
    'suit',
    'django.contrib.admin',
    'solo',

    # Django
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Files
    "filer",
    "mptt",
    "easy_thumbnails",

    # DDBB
    'reversion',
    # 'south',
    'import_export',

    # Staticfiles
    "compressor",
    'ckeditor',

    # Apps
    'shelfzilla.apps._admin',
    'shelfzilla.apps.config',
    'shelfzilla.apps.homepage',
    # 'shelfzilla.apps.landing',
    'shelfzilla.apps.mailing',
    'shelfzilla.apps.manga',
    'shelfzilla.apps.blog',
    'shelfzilla.apps.faq',
    'shelfzilla.apps.pjax',

    # API
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'shelfzilla.apps.pjax.context_processors.pjax',
    'shelfzilla.apps.manga.context_processors.user_have_volumes',
    'shelfzilla.apps.manga.context_processors.user_wishlisted_volumes',
    'shelfzilla.apps.manga.context_processors.user_read_volumes',
    'shelfzilla.apps.account.context_processors.auth',
    'shelfzilla.apps.account.context_processors.user_is_staff',
    # 'shelfzilla.apps.account.context_processors.user_configuration',
)

MIDDLEWARE_CLASSES = (
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'shelfzilla.middleware.BetaMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "themes", "_base"),
    os.path.join(BASE_DIR, "themes", "bootflat", "templates"),
)

ROOT_URLCONF = 'shelfzilla.urls'

WSGI_APPLICATION = 'shelfzilla.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGES = (
    ('es', _('Spanish')),
)

LANGUAGE_CODE = 'es'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "themes", "bootflat", "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/coffeescript', 'coffee --compile --stdio --no-header'),
)

# Max username length (longerusername)
MAX_USERNAME_LENGTH = 75

# Beta settings
# BETA_ACCESS_GROUP_ID = 1
# BETA_ACCESS_ALLOW_URLS = (
#     '/landing/',
#     '/login/',
#     '/messages/',
# )

# filer
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

COVER_FOLDER_PK = 1
COVER_FOLDER_OWNER_PK = 1

FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'django.core.files.storage.FileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(
                    os.path.join(MEDIA_ROOT, 'filer/public/')),
                'base_url': '/files/',
            },
            'UPLOAD_TO': 'shelfzilla.utils.filer_generate_randomized',
            'UPLOAD_TO_PREFIX': '',
        },
        'thumbnails': {
            'ENGINE': 'django.core.files.storage.FileSystemStorage',
            'OPTIONS': {
                'location': os.path.abspath(
                    os.path.join(MEDIA_ROOT, 'filer/public/')),
                'base_url': '/files/',
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

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}

#
#   ADMIN
#
SUIT_CONFIG = {
    'ADMIN_NAME': 'Shelfzilla',
    'SEARCH_URL': '',
    'MENU': (
        {
            'label': 'Authorization',
            'icon': 'icon-lock',
            'models': ('account.user', 'auth.group', 'account.accesscode', )
        },
        {
            'app': 'config',
            'label': 'Settings',
            'icon': 'icon-cog',
        },
        {
            'app': 'blog',
            'label': 'Blog',
            'icon': 'icon-book',
        },
        {
            'app': 'manga',
            'label': 'Manga',
            'icon': 'icon-book',
        },
        {
            'app': 'faq',
            'label': 'FAQs',
            'icon': 'icon-book',
        },
        {
            'label': 'Files',
            'icon': 'icon-file',
            'app': 'filer',
        },
    ),
}

#
#   CKEDITOR
#
CKEDITOR_UPLOAD_PATH = 'ckeditor/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Standard',
        'width': '100%',
    },
}

#
#   AUTH
#
AUTH_USER_MODEL = 'account.User'


#
#   API
#
CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

DJOSER = {
    'DOMAIN': 'shelfzilla.com',
    'SITE_NAME': 'Shelfzilla',
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'LOGIN_AFTER_ACTIVATION': True,
    'SEND_ACTIVATION_EMAIL': False,
}
