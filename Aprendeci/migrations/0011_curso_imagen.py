# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aprendeci', '0010_curso_sigla'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='imagen',
            field=models.ImageField(upload_to='img/cursos', default='img/cursos/Defecto.jpg'),
            preserve_default=True,
        ),
    ]
