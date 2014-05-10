# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='tags',
            field=models.ManyToManyField(to='tag.Tag'),
            preserve_default=True,
        ),
    ]
