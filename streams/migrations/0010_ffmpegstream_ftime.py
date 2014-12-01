# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0009_ffmpegstream_fposition'),
    ]

    operations = [
        migrations.AddField(
            model_name='ffmpegstream',
            name='ftime',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
