# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20141111_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=128, verbose_name='Code')),
                ('max_uses', models.IntegerField(default=1, verbose_name='Number of uses')),
                ('expiration', models.DateTimeField(default=None, null=True, verbose_name='Expires')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('user', models.ForeignKey(related_name='access_codes', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Access code',
                'verbose_name_plural': 'Access codes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='access_code',
            field=models.ForeignKey(related_name='used_by', blank=True, to='account.AccessCode', null=True),
            preserve_default=True,
        ),
    ]
