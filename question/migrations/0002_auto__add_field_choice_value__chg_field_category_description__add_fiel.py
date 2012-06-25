# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Choice.value'
        db.add_column('question_choice', 'value',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


        # Changing field 'Category.description'
        db.alter_column('question_category', 'description', self.gf('django.db.models.fields.TextField')(default=''))
        # Adding field 'Question.is_required'
        db.add_column('question_question', 'is_required',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'Question.question'
        db.alter_column('question_question', 'question', self.gf('django.db.models.fields.TextField')())
    def backwards(self, orm):
        # Deleting field 'Choice.value'
        db.delete_column('question_choice', 'value')


        # Changing field 'Category.description'
        db.alter_column('question_category', 'description', self.gf('django.db.models.fields.TextField')(null=True))
        # Deleting field 'Question.is_required'
        db.delete_column('question_question', 'is_required')


        # Changing field 'Question.question'
        db.alter_column('question_question', 'question', self.gf('django.db.models.fields.CharField')(max_length=255))
    models = {
        'question.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['question.Question']"})
        },
        'question.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'question.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['question.Question']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'question.question': {
            'Meta': {'object_name': 'Question'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['question.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'question_type': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['question']