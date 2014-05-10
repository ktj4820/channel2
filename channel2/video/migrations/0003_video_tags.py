# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_tag_tags'),
        ('video', '0002_videolink'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='tags',
            field=models.ManyToManyField(to='tag.Tag', null=True, blank=True),
            preserve_default=True,
        ),
    ]
