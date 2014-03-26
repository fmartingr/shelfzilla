# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Volume.for_review_comment'
        db.add_column(u'manga_volume', 'for_review_comment',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Publisher.for_review_comment'
        db.add_column(u'manga_publisher', 'for_review_comment',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Series.for_review_comment'
        db.add_column(u'manga_series', 'for_review_comment',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Volume.for_review_comment'
        db.delete_column(u'manga_volume', 'for_review_comment')

        # Deleting field 'Publisher.for_review_comment'
        db.delete_column(u'manga_publisher', 'for_review_comment')

        # Deleting field 'Series.for_review_comment'
        db.delete_column(u'manga_series', 'for_review_comment')


    models = {
        u'manga.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'for_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'for_review_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'manga.series': {
            'Meta': {'object_name': 'Series'},
            'for_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'for_review_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'manga.volume': {
            'Meta': {'object_name': 'Volume'},
            'for_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'for_review_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn_10': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'isbn_13': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manga.Publisher']"}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manga.Series']"})
        }
    }

    complete_apps = ['manga']