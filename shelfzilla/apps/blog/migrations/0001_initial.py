# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import ckeditor.fields
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('date', models.DateTimeField(default=datetime.datetime(2014, 11, 4, 22, 25, 34, 533640, tzinfo=utc))),
                ('content', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(max_length=128)),
                ('draft', models.BooleanField(default=True)),
                ('author', models.ForeignKey(related_name='author', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name_plural': 'Entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('color', models.CharField(max_length=6, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', null=True, blank=True),
            preserve_default=True,
        ),
    ]
