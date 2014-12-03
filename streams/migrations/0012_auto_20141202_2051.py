# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0011_auto_20141202_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ffmpegstream',
            name='srcip',
        ),
        migrations.AddField(
            model_name='ffmpegstream',
            name='fsrcip',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
