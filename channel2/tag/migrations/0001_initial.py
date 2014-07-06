# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100)),
                ('markdown', models.TextField(blank=True)),
                ('html', models.TextField(blank=True)),
                ('pinned', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('children', models.ManyToManyField(editable=False, blank=True, to='tag.Tag', null=True)),
                ('updated_by', models.ForeignKey(editable=False, null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('users', models.ManyToManyField(editable=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'tag',
            },
            bases=(models.Model,),
        ),
    ]
