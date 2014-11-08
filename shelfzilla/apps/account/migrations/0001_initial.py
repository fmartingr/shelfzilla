# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(help_text='An user email that should be verified.', unique=True, max_length=255, verbose_name='Email address', db_index=True)),
                ('username', models.CharField(null=True, default=None, max_length=128, blank=True, unique=True, verbose_name='Username', db_index=True)),
                ('first_name', models.CharField(default=b'', max_length=80, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(default=b'', max_length=80, verbose_name='Last name', blank=True)),
                ('birthdate', models.DateField(default=None, null=True, verbose_name='Birthdate', blank=True)),
                ('gender', models.CharField(default=b'', max_length=80, verbose_name='Gender', blank=True, choices=[(b'male', 'Male'), (b'female', 'Female')])),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date joined')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Active status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Staff status')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
            },
            bases=(models.Model,),
        ),
    ]
