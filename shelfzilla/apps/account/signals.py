# coding: utf-8

# django
from django.dispatch import Signal
from django.dispatch import receiver


user_registered = Signal(providing_args=["user"])


@receiver(user_registered)
def send_email_new_user(sender, **kwargs):
    from shelfzilla.apps.mailing.emails import RegistrationEmail
    mail = RegistrationEmail({"user": kwargs.get('user')})
    mail.send()
