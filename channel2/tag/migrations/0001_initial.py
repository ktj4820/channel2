# encoding: utf8
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('markdown', models.TextField(blank=True)),
                ('html', models.TextField(blank=True)),
                ('pinned', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, to_field='id')),
            ],
            options={
                'db_table': 'tag',
            },
            bases=(models.Model,),
        ),
    ]
