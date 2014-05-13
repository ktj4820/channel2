# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_tag_tags'),
        ('video', '0002_videolink'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to_field='id', blank=True, to='tag.Tag'),
            preserve_default=True,
        ),
    ]
