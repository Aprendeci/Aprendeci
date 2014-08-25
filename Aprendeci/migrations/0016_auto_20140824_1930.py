# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0015_auto_20140824_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concepto',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='img/icons/conceptos'),
        ),
    ]
