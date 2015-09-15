# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from channel2.tag.enums import TagType
from channel2.tag.utils import season_re


def set_season_tag_type(apps, schema_editor):
    Tag = apps.get_model('tag', 'Tag')
    for tag in Tag.objects.all():
        match = season_re.match(tag.name)
        if not match: continue

        tag.type = TagType.SEASON
        tag.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(set_season_tag_type)
    ]
