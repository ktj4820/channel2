# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videolink',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+'),
        ),
        migrations.AlterField(
            model_name='videolink',
            name='created_on',
            field=models.DateTimeField(db_index=True, auto_now_add=True),
        ),
    ]