# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0003_auto_20140929_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ffmpegstream',
            name='fapp',
        ),
        migrations.RemoveField(
            model_name='ffmpegstream',
            name='fip',
        ),
        migrations.RemoveField(
            model_name='ffmpegstream',
            name='fstream',
        ),
        migrations.AddField(
            model_name='ffmpegstream',
            name='fpid',
            field=models.CharField(default=-1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ffmpegstream',
            name='ftreename',
            field=models.CharField(default=111, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ffmpegstream',
            name='fuserCount',
            field=models.CharField(default=-1, max_length=10),
            preserve_default=False,
        ),
    ]
