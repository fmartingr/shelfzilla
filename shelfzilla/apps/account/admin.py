# -*- coding: utf-8 -*-
"""
License boilerplate should be used here.
"""

# python 3 imports
from __future__ import absolute_import, unicode_literals

# python imports
import logging

# django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _

# app imports
from . import models

logger = logging.getLogger(__name__)


class UserAdmin(DjangoUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'email', 'username', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'birthdate', 'gender', )}),
        (_('Permissions'), {'fields': ('is_staff', 'user_permissions')}),
        (_('Information'), {'fields': ('date_joined', 'last_login', )})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('user_permissions', )
    readonly_fields = ('date_joined', 'last_login', )

# Now register the new UserAdmin...
admin.site.register(models.User, UserAdmin)
admin.site.register(Permission)
