# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0008_curso_grafo'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='clave',
            field=models.CharField(max_length=100, default=1),
            preserve_default=False,
        ),
    ]
