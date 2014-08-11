# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Aprendeci', '0006_recurso_concepto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('estudiantes', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('profesor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
