# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concepto',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=500)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('imagen', models.ImageField(upload_to='img/icons/conceptos')),
                ('x', models.IntegerField(default=0)),
                ('y', models.IntegerField(default=0)),
                ('requisitos', models.ManyToManyField(to='Aprendeci.Concepto', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grafo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=500)),
                ('grafoPadre', models.ForeignKey(to='Aprendeci.Grafo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='concepto',
            name='grafo',
            field=models.ForeignKey(to='Aprendeci.Grafo', blank=True),
            preserve_default=True,
        ),
    ]
