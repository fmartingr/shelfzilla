# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SocialConfiguration.facebook_url'
        db.add_column(u'config_socialconfiguration', 'facebook_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'SocialConfiguration.google_plus_url'
        db.add_column(u'config_socialconfiguration', 'google_plus_url',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'SocialConfiguration.contact_email'
        db.add_column(u'config_socialconfiguration', 'contact_email',
                      self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SocialConfiguration.facebook_url'
        db.delete_column(u'config_socialconfiguration', 'facebook_url')

        # Deleting field 'SocialConfiguration.google_plus_url'
        db.delete_column(u'config_socialconfiguration', 'google_plus_url')

        # Deleting field 'SocialConfiguration.contact_email'
        db.delete_column(u'config_socialconfiguration', 'contact_email')


    models = {
        u'config.siteconfiguration': {
            'Meta': {'object_name': 'SiteConfiguration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maintenance_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'config.socialconfiguration': {
            'Meta': {'object_name': 'SocialConfiguration'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'facebook_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'google_analytics': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'google_plus_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'twitter_account': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['config']