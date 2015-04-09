# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manga', '0001_initial'),
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='translatedquestion',
            name='language',
            field=models.ForeignKey(default=1, to='manga.Language'),
            preserve_default=False,
        ),
    ]
