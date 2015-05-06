# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('views', models.IntegerField(default=0)),
                ('cover', models.CharField(max_length=300, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
