"""
WSGI config for shelfzilla project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os


SETTINGS_FILE = 'local'
if 'ENVIRONMENT' in os.environ:
    SETTINGS_FILE = os.environ['ENVIRONMENT']


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "shelfzilla.settings.{}".format(SETTINGS_FILE)
)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
