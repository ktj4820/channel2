# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagChildren',
            fields=[
            ],
            options={
                'db_table': 'tag_children',
                'verbose_name_plural': 'Tag children',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tag',
            name='created_by',
            field=models.ForeignKey(related_name='+', null=True, editable=False, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 1, 22, 33, 37, 514676), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tag',
            name='children',
            field=models.ManyToManyField(editable=False, null=True, to='tag.Tag', related_name='parents', blank=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='updated_by',
            field=models.ForeignKey(related_name='+', null=True, editable=False, to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='users',
            field=models.ManyToManyField(editable=False, null=True, to=settings.AUTH_USER_MODEL, related_name='pinned_tags', blank=True),
        ),
    ]
