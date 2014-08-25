# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0014_auto_20140810_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='concepto',
            name='color',
            field=models.CharField(default='A22F38', max_length=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='curso',
            name='estudiantes',
            field=models.ManyToManyField(to='Aprendeci.Estudiante', related_name='estudiantes'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='profesor',
            field=models.ForeignKey(to='Aprendeci.Profesor', related_name='profesor'),
        ),
    ]
