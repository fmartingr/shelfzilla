# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionanswer',
            options={'ordering': ('ord',), 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='questionanswercategory',
            options={'ordering': ('name_es',), 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='questionanswer',
            name='category',
            field=models.ForeignKey(related_name='questions', to='faq.QuestionAnswerCategory'),
            preserve_default=True,
        ),
    ]
