# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('question_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('question', ['Category'])

        # Adding model 'Question'
        db.create_table('question_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['question.Category'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('question_type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('question', ['Question'])

        # Adding model 'Choice'
        db.create_table('question_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['question.Question'])),
            ('choice', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('question', ['Choice'])

        # Adding model 'Answer'
        db.create_table('question_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['question.Question'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('question', ['Answer'])

    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('question_category')

        # Deleting model 'Question'
        db.delete_table('question_question')

        # Deleting model 'Choice'
        db.delete_table('question_choice')

        # Deleting model 'Answer'
        db.delete_table('question_answer')

    models = {
        'question.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['question.Question']"})
        },
        'question.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'question.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['question.Question']"})
        },
        'question.question': {
            'Meta': {'object_name': 'Question'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['question.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question_type': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['question']