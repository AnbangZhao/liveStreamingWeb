# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0007_videoquality'),
    ]

    operations = [
        migrations.AddField(
            model_name='ffmpegstream',
            name='fRtspSource',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
