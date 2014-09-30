# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0018_auto_20140824_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='grafo',
            name='x',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grafo',
            name='y',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
