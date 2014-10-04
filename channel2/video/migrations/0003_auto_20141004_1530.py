# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20141002_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='tag',
            field=models.ForeignKey(to='tag.Tag', null=True, blank=True),
        ),
    ]
