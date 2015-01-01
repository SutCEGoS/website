# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Course.level'
        db.delete_column(u'course_course', 'level')

        # Deleting field 'OfferedCourse.class_time'
        db.delete_column(u'course_offeredcourse', 'class_time')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Course.level'
        raise RuntimeError("Cannot reverse this migration. 'Course.level' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'OfferedCourse.class_time'
        raise RuntimeError("Cannot reverse this migration. 'OfferedCourse.class_time' and its values cannot be restored.")

    models = {
        u'base.educationalyear': {
            'Meta': {'object_name': 'EducationalYear'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'course.course': {
            'Meta': {'object_name': 'Course'},
            'course_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'course.field': {
            'Meta': {'object_name': 'Field'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'course.offeredcourse': {
            'Meta': {'unique_together': "(('course', 'group_number', 'term', 'year'),)", 'object_name': 'OfferedCourse'},
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Course']"}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'exam_time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'group_number': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['course.Professor']"}),
            'term': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.EducationalYear']"})
        },
        u'course.professor': {
            'Meta': {'object_name': 'Professor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['course']