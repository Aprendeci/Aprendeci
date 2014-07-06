# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0002_auto_20140705_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='concepto',
            name='grafo',
            field=models.ForeignKey(to='Aprendeci.Grafo', blank=True, default=1),
            preserve_default=False,
        ),
    ]
