# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Publisher.url'
        db.add_column(u'manga_publisher', 'url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Publisher.url'
        db.delete_column(u'manga_publisher', 'url')


    models = {
        u'manga.publisher': {
            'Meta': {'ordering': "['name']", 'object_name': 'Publisher'},
            'for_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'for_review_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'manga.series': {
            'Meta': {'ordering': "['name']", 'object_name': 'Series'},
            'for_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'for_review_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'manga.volume': {
            'Meta': {'ordering': "['series__name', 'number']", 'object_name': 'Volume'},
            'for_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'for_review_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn_10': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'isbn_13': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'volumes'", 'to': u"orm['manga.Publisher']"}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'volumes'", 'to': u"orm['manga.Series']"})
        }
    }

    complete_apps = ['manga']