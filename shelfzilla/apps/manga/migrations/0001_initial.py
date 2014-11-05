# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('filer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('code', models.CharField(max_length=5, verbose_name='Code')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('for_review', models.BooleanField(default=False, verbose_name='For review')),
                ('for_review_comment', models.TextField(null=True, verbose_name='Review comment', blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('slug', models.SlugField(null=True, verbose_name='Slug', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('for_review', models.BooleanField(default=False, verbose_name='For review')),
                ('for_review_comment', models.TextField(null=True, verbose_name='Review comment', blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', models.SlugField(null=True, verbose_name='Slug', blank=True)),
                ('url', models.URLField(null=True, verbose_name='URL', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Publisher',
                'verbose_name_plural': 'Publishers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('for_review', models.BooleanField(default=False, verbose_name='For review')),
                ('for_review_comment', models.TextField(null=True, verbose_name='Review comment', blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('slug', models.SlugField(max_length=256, null=True, verbose_name='Slug', blank=True)),
                ('summary', models.TextField(null=True, verbose_name='Summary', blank=True)),
                ('finished', models.BooleanField(default=False, verbose_name='Finished')),
                ('status', models.CharField(default=b'open', max_length=16, verbose_name='Status', choices=[(b'open', 'Open'), (b'finished', 'Finished'), (b'cancelled', 'Cancelled'), (b'on-hold', 'On-hold')])),
                ('art', models.ManyToManyField(related_name='artist_of', null=True, to='manga.Person', blank=True)),
                ('cover', filer.fields.image.FilerImageField(blank=True, to='filer.Image', null=True)),
                ('folder', models.ForeignKey(blank=True, to='filer.Folder', null=True)),
                ('original_publisher', models.ForeignKey(related_name='original_series', blank=True, to='manga.Publisher', null=True)),
                ('story', models.ManyToManyField(related_name='scriptwriter_of', null=True, to='manga.Person', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Series',
                'verbose_name_plural': 'Series',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeriesPublisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('for_review', models.BooleanField(default=False, verbose_name='For review')),
                ('for_review_comment', models.TextField(null=True, verbose_name='Review comment', blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('status', models.CharField(default=b'open', max_length=16, verbose_name='Status', choices=[(b'open', 'Open'), (b'finished', 'Finished'), (b'cancelled', 'Cancelled'), (b'on-hold', 'On-hold')])),
                ('actual_publisher', models.BooleanField(default=True, verbose_name='Current publisher')),
                ('publisher', models.ForeignKey(related_name='series_published', to='manga.Publisher')),
                ('series', models.ForeignKey(related_name='publishers', to='manga.Series')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeriesSummary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('for_review', models.BooleanField(default=False, verbose_name='For review')),
                ('for_review_comment', models.TextField(null=True, verbose_name='Review comment', blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('summary', models.TextField(null=True, verbose_name='Summary', blank=True)),
                ('language', models.ForeignKey(to='manga.Language')),
                ('series', models.ForeignKey(related_name='summaries', to='manga.Series')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserHaveVolume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('user', models.ForeignKey(related_name='have_volumes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('volume__series__name', 'volume__number'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserReadVolume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('user', models.ForeignKey(related_name='read_volumes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('volume__series__name', 'volume__number'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserWishlistVolume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('user', models.ForeignKey(related_name='wishlisted_volumes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('volume__series__name', 'volume__number'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('for_review', models.BooleanField(default=False, verbose_name='For review')),
                ('for_review_comment', models.TextField(null=True, verbose_name='Review comment', blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('number', models.IntegerField(null=True, verbose_name='Number', blank=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name='Name', blank=True)),
                ('isbn_10', models.CharField(max_length=10, null=True, verbose_name='ISBN-10', blank=True)),
                ('isbn_13', models.CharField(max_length=13, null=True, verbose_name='ISBN-13', blank=True)),
                ('retail_price', models.DecimalField(null=True, verbose_name='Retail price', max_digits=5, decimal_places=2, blank=True)),
                ('pages', models.IntegerField(null=True, verbose_name='Pages', blank=True)),
                ('release_date', models.DateField(null=True, verbose_name='Release date')),
            ],
            options={
                'ordering': ['series__name', 'language', 'number'],
                'verbose_name': 'Volume',
                'verbose_name_plural': 'Volumes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VolumeCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('for_review', models.BooleanField(default=False, verbose_name='For review')),
                ('for_review_comment', models.TextField(null=True, verbose_name='Review comment', blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('default', models.BooleanField(default=True, verbose_name='Default')),
                ('series', models.ForeignKey(related_name='collections', to='manga.Series')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='volume',
            name='collection',
            field=models.ForeignKey(related_name='volumes', to='manga.VolumeCollection', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='volume',
            name='cover',
            field=filer.fields.image.FilerImageField(blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='volume',
            name='language',
            field=models.ForeignKey(to='manga.Language', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='volume',
            name='publisher',
            field=models.ForeignKey(related_name='volumes', to='manga.Publisher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='volume',
            name='series',
            field=models.ForeignKey(related_name='volumes', to='manga.Series'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userwishlistvolume',
            name='volume',
            field=models.ForeignKey(related_name='wishlisted_by', to='manga.Volume'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userreadvolume',
            name='volume',
            field=models.ForeignKey(related_name='read_by', to='manga.Volume'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userhavevolume',
            name='volume',
            field=models.ForeignKey(related_name='owned_by', to='manga.Volume'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='seriessummary',
            unique_together=set([('series', 'language')]),
        ),
    ]
