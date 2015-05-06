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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'Tag children',
                'managed': False,
                'db_table': 'tag_children',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200)),
                ('type', models.CharField(max_length=20, choices=[('anime', 'Anime'), ('common', 'Common')], default='common')),
                ('markdown', models.TextField(blank=True)),
                ('html', models.TextField(blank=True)),
                ('json', jsonfield.fields.JSONField(default={})),
                ('pinned', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('cover', models.CharField(max_length=300, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('children', models.ManyToManyField(blank=True, related_name='parents', to='tag.Tag')),
            ],
            options={
                'db_table': 'tag',
            },
        ),
    ]
