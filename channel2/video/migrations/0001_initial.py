# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import channel2.core.uploads
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('file', models.FileField(upload_to=channel2.core.uploads.video_file_upload_to, blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(editable=False, max_length=100)),
                ('views', models.IntegerField(default=0)),
                ('cover', models.FileField(upload_to=channel2.core.uploads.video_cover_upload_to, blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('tag', models.ForeignKey(to='tag.Tag', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'db_table': 'video',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoLink',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('key', models.CharField(max_length=64, db_index=True)),
                ('ip_address', models.CharField(max_length=64)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(to='video.Video')),
            ],
            options={
                'db_table': 'video_link',
            },
            bases=(models.Model,),
        ),
    ]
