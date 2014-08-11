# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Aprendeci', '0013_auto_20140810_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='curso',
            name='profesor',
            field=models.ForeignKey(to='Aprendeci.Estudiante'),
        ),
    ]
