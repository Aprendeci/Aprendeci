# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0007_curso'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='grafo',
            field=models.ForeignKey(to='Aprendeci.Grafo', default=1),
            preserve_default=False,
        ),
    ]
