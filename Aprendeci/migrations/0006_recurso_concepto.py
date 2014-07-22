# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0005_recurso'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurso',
            name='concepto',
            field=models.ForeignKey(default=1, to='Aprendeci.Concepto'),
            preserve_default=False,
        ),
    ]
