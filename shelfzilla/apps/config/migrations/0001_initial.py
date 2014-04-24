# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteConfiguration'
        db.create_table(u'config_siteconfiguration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('maintenance_mode', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'config', ['SiteConfiguration'])

        # Adding model 'SocialConfiguration'
        db.create_table(u'config_socialconfiguration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('twitter_account', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('google_analytics', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'config', ['SocialConfiguration'])


    def backwards(self, orm):
        # Deleting model 'SiteConfiguration'
        db.delete_table(u'config_siteconfiguration')

        # Deleting model 'SocialConfiguration'
        db.delete_table(u'config_socialconfiguration')


    models = {
        u'config.siteconfiguration': {
            'Meta': {'object_name': 'SiteConfiguration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maintenance_mode': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'config.socialconfiguration': {
            'Meta': {'object_name': 'SocialConfiguration'},
            'google_analytics': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'twitter_account': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['config']