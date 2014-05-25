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
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', models.SlugField(editable=False, max_length=100)),
                ('markdown', models.TextField(blank=True)),
                ('html', models.TextField(blank=True)),
                ('pinned', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'label',
                'ordering': ('slug',),
            },
            bases=(models.Model,),
        ),
    ]
