# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Aprendeci', '0011_curso_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calificaciones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calificacion', models.IntegerField()),
                ('concepto', models.ForeignKey(to='Aprendeci.Concepto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='calificaciones',
            name='estudiante',
            field=models.ForeignKey(to='Aprendeci.Estudiante'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='estudiante',
            name='conceptos',
            field=models.ManyToManyField(to='Aprendeci.Concepto', through='Aprendeci.Calificaciones'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='estudiante',
            name='usuario',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='concepto',
            name='porcentajeBase',
            field=models.IntegerField(default=60),
            preserve_default=True,
        ),
    ]
