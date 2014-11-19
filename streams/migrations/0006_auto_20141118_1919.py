# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0005_auto_20141118_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ffmpegstream',
            name='id',
        ),
        migrations.AlterField(
            model_name='ffmpegstream',
            name='ftreename',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
    ]
