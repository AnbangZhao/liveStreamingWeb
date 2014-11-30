# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0008_ffmpegstream_frtspsource'),
    ]

    operations = [
        migrations.AddField(
            model_name='ffmpegstream',
            name='fposition',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
