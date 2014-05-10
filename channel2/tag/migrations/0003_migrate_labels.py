# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_labels(apps, schema_editor):
    Tag = apps.get_model('tag', 'Tag')
    Label = apps.get_model('label', 'Label')

    for label in Label.objects.all():
        tag = Tag.objects.create(name=label.name, slug=label.slug, markdown=label.markdown, html=label.html)
        for video in label.video_set.all():
            video.tags.add(tag)


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0002_tag_tags'),
        ('video', '0003_video_tags'),
    ]

    operations = [
        migrations.RunPython(migrate_labels),
    ]
