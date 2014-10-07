# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0002_ffmpegstream'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ffmpegstream',
            old_name='app',
            new_name='fapp',
        ),
        migrations.RenameField(
            model_name='ffmpegstream',
            old_name='ip',
            new_name='fip',
        ),
        migrations.RenameField(
            model_name='ffmpegstream',
            old_name='stream',
            new_name='fstream',
        ),
    ]
