# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0006_auto_20141118_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='videoQuality',
            fields=[
                ('sVideo', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('sQuality', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
