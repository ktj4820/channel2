# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_labels(apps, schema_editor):
    Tag = apps.get_model('tag', 'Tag')
    Label = apps.get_model('label', 'Label')

    label_list = Label.objects.all()
    for label in label_list:
        tag = Tag.objects.create(name=label.name, slug=label.slug, markdown=label.markdown, html=label.html, pinned=label.pinned)
        for video in label.video_set.all():
            video.tag = tag
            video.save()

    tag_list = Tag.objects.all()
    tag_dict = {t.name: t for t in tag_list}
    for label in label_list.select_related('parent'):
        if not label.parent: continue
        tag_child = tag_dict[label.parent.name]
        tag = tag_dict[label.name]
        tag.children.add(tag_child)


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0002_label_parent'),
        ('tag', '0002_tag_children_users'),
        ('video', '0003_video_tag'),
    ]

    operations = [
        migrations.RunPython(migrate_labels),
    ]
