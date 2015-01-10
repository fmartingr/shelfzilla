# coding: utf-8
from hashlib import md5

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser,
           PermissionsMixin):
    """

    """
    MALE = 'male'
    FEMALE = 'female'
    GENDER_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    )

    @property
    def avatar(self):
        avatar = '{}{}?s=300'.format(
            'https://www.gravatar.com/avatar/',
            md5(self.email.lower()).hexdigest()
        )
        return avatar

    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_('An user email that should be verified.')
    )

    username = models.CharField(
        verbose_name=_('Username'),
        max_length=128,
        unique=True,
        db_index=True,
    )

    # personal info
    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=80, blank=True, default='',
    )

    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=80, blank=True, default='',
    )

    birthdate = models.DateField(
        verbose_name=_('Birthdate'),
        null=True,
        blank=True,
        default=None,
    )

    gender = models.CharField(
        verbose_name=_('Gender'),
        max_length=80,
        choices=GENDER_CHOICES,
        blank=True,
        default=''
    )

    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        auto_now_add=True,
        editable=False,
    )

    is_active = models.BooleanField(
        verbose_name=_('Active status'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    )

    is_staff = models.BooleanField(
        verbose_name=_('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.')
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    # Access codes / Invitations
    access_code = models.ForeignKey('account.AccessCode',
                                    null=True, blank=True,
                                    related_name='used_by')

    objects = UserManager()

    class Meta:
        verbose_name = _('User')

    def __unicode__(self):
        return unicode(self.username) or unicode(self.email)

    @property
    def is_confirmed(self):
        return self.CONFIRMED == self.status

    @property
    def full_name(self):
        return '{first_name} {last_name}'.format(
            first_name=self.first_name.strip(),
            last_name=self.last_name.strip()
        )

    @property
    def age(self):
        """Age of the user

        Returns the age of the user if she has a defined birthdate.
        """
        if self.birthdate is None:
            return None
        else:
            today = timezone.now()
            birthdate = self.birthdate
            try:
                birthdate.replace(year=today.year)
            except ValueError:
                # Raises only with 29th February and current not leap year
                birthdate_day = 28
            else:
                birthdate_day = birthdate.day
            return today.year - birthdate.year - (
                (today.month, today.day) < (birthdate.month, birthdate_day)
            )


class AccessCode(models.Model):
    code = models.CharField(_('Code'), max_length=128)
    max_uses = models.IntegerField(_('Number of uses'), default=1)
    user = models.ForeignKey(User, null=True, blank=True,
                             related_name='access_codes')
    expiration = models.DateTimeField(_('Expires'), null=True, blank=True,
                                      default=None)
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Access code')
        verbose_name_plural = _('Access codes')

    def __unicode__(self):
        return self.code

    @property
    def usabe(self):
        # Check if active
        if not self.active:
            return False

        # Check if expired
        if timezone.now() >= self.expiration:
            return False

        # Check if it someone already used it
        if self.used_by.count() == self.max_uses:
            return False

        return True
