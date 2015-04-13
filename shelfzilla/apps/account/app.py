# coding: utf-8

# py3
from __future__ import absolute_import

# django
from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'
    verbose_name = "Account"

    def ready(self):
        from . import signals
