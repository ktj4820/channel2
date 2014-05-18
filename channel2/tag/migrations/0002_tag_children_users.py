# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='children',
            field=models.ManyToManyField(null=True, to='tag.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='users',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
