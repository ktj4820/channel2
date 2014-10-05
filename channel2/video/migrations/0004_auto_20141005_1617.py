# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_auto_20141004_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='tag',
            field=models.ForeignKey(to='tag.Tag'),
        ),
    ]
