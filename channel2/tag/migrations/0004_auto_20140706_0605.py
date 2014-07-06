# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0003_migrate_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='children',
            field=models.ManyToManyField(null=True, to='tag.Tag', editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='updated_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='tag',
            name='users',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, editable=False, blank=True),
        ),
    ]
