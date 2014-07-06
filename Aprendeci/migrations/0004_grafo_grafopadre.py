# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0003_concepto_grafo'),
    ]

    operations = [
        migrations.AddField(
            model_name='grafo',
            name='grafoPadre',
            field=models.ForeignKey(blank=True, to='Aprendeci.Grafo', null=True),
            preserve_default=True,
        ),
    ]
