# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Concepto'
        db.create_table('Aprendeci_concepto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('fecha_creacion', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('x', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('y', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('Aprendeci', ['Concepto'])

        # Adding M2M table for field requisitos on 'Concepto'
        m2m_table_name = db.shorten_name('Aprendeci_concepto_requisitos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_concepto', models.ForeignKey(orm['Aprendeci.concepto'], null=False)),
            ('to_concepto', models.ForeignKey(orm['Aprendeci.concepto'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_concepto_id', 'to_concepto_id'])


    def backwards(self, orm):
        # Deleting model 'Concepto'
        db.delete_table('Aprendeci_concepto')

        # Removing M2M table for field requisitos on 'Concepto'
        db.delete_table(db.shorten_name('Aprendeci_concepto_requisitos'))


    models = {
        'Aprendeci.concepto': {
            'Meta': {'object_name': 'Concepto'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'requisitos': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'requisitos_rel_+'", 'to': "orm['Aprendeci.Concepto']"}),
            'x': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['Aprendeci']