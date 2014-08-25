# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0017_auto_20140824_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concepto',
            name='imagen',
            field=models.ImageField(upload_to='img/icons/conceptos', default='img/icons/conceptos/defecto.png'),
        ),
    ]
