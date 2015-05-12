# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('file', models.CharField(max_length=300, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('episode', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('views', models.IntegerField(default=0)),
                ('cover', models.CharField(blank=True, max_length=300)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('tag', models.ForeignKey(to='tag.Tag')),
            ],
            options={
                'db_table': 'video',
            },
        ),
        migrations.CreateModel(
            name='VideoLink',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('key', models.CharField(max_length=64, unique=True)),
                ('ip_address', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
                ('video', models.ForeignKey(to='video.Video')),
            ],
            options={
                'db_table': 'video_link',
            },
        ),
    ]
