# coding: utf-8

from django.utils.translation import ugettext_lazy as _

from .models import Email


class RegistrationEmail(Email):
    template = 'mailing/registration.html'
    subject = _('Bienvenido a Shelfzilla')

    # Context requires:
    # - user: <User model>

    def prepare(self):
        self.recipients.append(self.context['user'].email)
