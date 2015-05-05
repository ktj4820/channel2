# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TagChildren',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'db_table': 'tag_children',
                'verbose_name_plural': 'Tag children',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200)),
                ('type', models.CharField(max_length=20, choices=[('anime', 'Anime'), ('common', 'Common')])),
                ('markdown', models.TextField(blank=True)),
                ('html', models.TextField(blank=True)),
                ('json', jsonfield.fields.JSONField(default={})),
                ('pinned', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('cover', models.CharField(blank=True, max_length=300)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('children', models.ManyToManyField(blank=True, to='tag.Tag', related_name='parents')),
            ],
            options={
                'db_table': 'tag',
            },
        ),
    ]
