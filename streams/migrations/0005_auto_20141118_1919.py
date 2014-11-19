# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0004_auto_20141118_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publisher',
            name='id',
        ),
        migrations.AlterField(
            model_name='publisher',
            name='name',
            field=models.CharField(max_length=30, serialize=False, primary_key=True),
        ),
    ]
