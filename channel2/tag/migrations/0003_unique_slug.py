# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_set_season_tag_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='tag',
            name='type',
            field=models.CharField(choices=[('anime', 'Anime'), ('common', 'Common'), ('season', 'Season')], max_length=20, default='common'),
        ),
    ]
