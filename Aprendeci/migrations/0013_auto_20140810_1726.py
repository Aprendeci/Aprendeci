# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0012_auto_20140810_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='estudiantes',
            field=models.ManyToManyField(to='Aprendeci.Estudiante'),
        ),
    ]
