# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0016_auto_20140824_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concepto',
            name='imagen',
            field=models.ImageField(default='img/icons/defecto.png', upload_to='img/icons/conceptos'),
        ),
    ]
