# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import channel2.core.uploads
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagChildren',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Tag children',
                'db_table': 'tag_children',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tag',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=channel2.core.uploads.tag_cover_upload_to),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='sort_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='children',
            field=models.ManyToManyField(blank=True, editable=False, to='tag.Tag', null=True, related_name='parents'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='users',
            field=models.ManyToManyField(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, related_name='pinned_tags'),
        ),
    ]
