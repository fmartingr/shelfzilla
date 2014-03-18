# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Publisher'
        db.create_table(u'manga_publisher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_review', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'manga', ['Publisher'])

        # Adding model 'Series'
        db.create_table(u'manga_series', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_review', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'manga', ['Series'])

        # Adding model 'Volume'
        db.create_table(u'manga_volume', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('for_review', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manga.Series'])),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manga.Publisher'])),
            ('isbn_10', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('isbn_13', self.gf('django.db.models.fields.CharField')(max_length=13, null=True, blank=True)),
        ))
        db.send_create_signal(u'manga', ['Volume'])


    def backwards(self, orm):
        # Deleting model 'Publisher'
        db.delete_table(u'manga_publisher')

        # Deleting model 'Series'
        db.delete_table(u'manga_series')

        # Deleting model 'Volume'
        db.delete_table(u'manga_volume')


    models = {
        u'manga.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'for_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'manga.series': {
            'Meta': {'object_name': 'Series'},
            'for_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'manga.volume': {
            'Meta': {'object_name': 'Volume'},
            'for_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn_10': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'isbn_13': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manga.Publisher']"}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manga.Series']"})
        }
    }

    complete_apps = ['manga']