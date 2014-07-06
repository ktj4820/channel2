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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100)),
                ('markdown', models.TextField(blank=True)),
                ('html', models.TextField(blank=True)),
                ('pinned', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('children', models.ManyToManyField(editable=False, null=True, blank=True, to='tag.Tag')),
                ('updated_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, blank=True, null=True)),
                ('users', models.ManyToManyField(editable=False, null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tag',
            },
            bases=(models.Model,),
        ),
    ]
