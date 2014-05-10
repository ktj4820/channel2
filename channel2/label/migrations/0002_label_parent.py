# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='parent',
            field=models.ForeignKey(blank=True, to='label.Label', to_field='id', null=True),
            preserve_default=True,
        ),
    ]
