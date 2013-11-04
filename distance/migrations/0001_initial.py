# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

try:
    from localflavor.us.models import USStateField
    us_state_field = 'localflavor.us.models.USStateField'
except ImportError:
    from django.contrib.localflavor.us.models import USStateField
    us_state_field = 'django.contrib.localflavor.us.models.USStateField'


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Zip'
        db.create_table(u'distance_zip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('state', self.gf(us_state_field)(max_length=2)),
        ))
        db.send_create_signal(u'distance', ['Zip'])


    def backwards(self, orm):
        # Deleting model 'Zip'
        db.delete_table(u'distance_zip')


    models = {
        u'distance.zip': {
            'Meta': {'ordering': "['code']", 'object_name': 'Zip'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'state': (us_state_field, [], {'max_length': '2'})
        }
    }

    complete_apps = ['distance']
