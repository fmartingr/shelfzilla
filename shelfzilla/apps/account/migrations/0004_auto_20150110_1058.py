# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150110_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesscode',
            name='expiration',
            field=models.DateTimeField(default=None, null=True, verbose_name='Expires', blank=True),
            preserve_default=True,
        ),
    ]
