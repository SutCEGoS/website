# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'EventRegister.std_number'
        db.delete_column(u'event_eventregister', 'std_number')

        # Adding field 'EventRegister.std_id'
        db.add_column(u'event_eventregister', 'std_id',
                      self.gf('django.db.models.fields.CharField')(default='--', max_length=63),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'EventRegister.std_number'
        raise RuntimeError("Cannot reverse this migration. 'EventRegister.std_number' and its values cannot be restored.")
        # Deleting field 'EventRegister.std_id'
        db.delete_column(u'event_eventregister', 'std_id')


    models = {
        u'event.event': {
            'Meta': {'object_name': 'Event'},
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'reg_end': ('django.db.models.fields.DateTimeField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'event.eventregister': {
            'Meta': {'object_name': 'EventRegister'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'std_id': ('django.db.models.fields.CharField', [], {'max_length': '63'})
        }
    }

    complete_apps = ['event']