#!/usr/bin/env python
import os
import sys

SETTINGS_FILE = 'local'
if 'ENVIRONMENT' in os.environ:
    SETTINGS_FILE = os.environ['ENVIRONMENT']

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "shelfzilla.settings.{}".format(SETTINGS_FILE)
    )

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
