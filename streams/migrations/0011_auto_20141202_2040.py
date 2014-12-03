# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0010_ffmpegstream_ftime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ffmpegstream',
            name='fRtspSource',
        ),
        migrations.AddField(
            model_name='ffmpegstream',
            name='srcip',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
