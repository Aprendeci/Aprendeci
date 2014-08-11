# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0009_curso_clave'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='sigla',
            field=models.CharField(default=1, max_length=4),
            preserve_default=False,
        ),
    ]
