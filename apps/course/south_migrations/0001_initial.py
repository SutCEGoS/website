# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Professor'
        db.create_table(u'course_professor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'course', ['Professor'])

        # Adding model 'Field'
        db.create_table(u'course_field', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'course', ['Field'])

        # Adding model 'Course'
        db.create_table(u'course_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('course_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'course', ['Course'])

        # Adding model 'OfferedCourse'
        db.create_table(u'course_offeredcourse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Course'])),
            ('professor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['course.Professor'])),
            ('group_number', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('term', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('year', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.EducationalYear'])),
            ('exam_time', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('class_time', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')()),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=1023)),
        ))
        db.send_create_signal(u'course', ['OfferedCourse'])

        # Adding unique constraint on 'OfferedCourse', fields ['course', 'group_number', 'term', 'year']
        db.create_unique(u'course_offeredcourse', ['course_id', 'group_number', 'term', 'year_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'OfferedCourse', fields ['course', 'group_number', 'term', 'year']
        db.delete_unique(u'course_offeredcourse', ['course_id', 'group_number', 'term', 'year_id'])

        # Deleting model 'Professor'
        db.delete_table(u'course_professor')

        # Deleting model 'Field'
        db.delete_table(u'course_field')

        # Deleting model 'Course'
        db.delete_table(u'course_course')

        # Deleting model 'OfferedCourse'
        db.delete_table(u'course_offeredcourse')


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
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
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
            'class_time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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