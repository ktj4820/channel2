import os

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from jsonfield.fields import JSONField

from channel2.core.utils import slugify, remove_media_file
from channel2.settings import MEDIA_URL, STATIC_URL
from channel2.tag.enums import TagType


class Tag(models.Model):

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200)
    type = models.CharField(choices=TagType.choices, max_length=20, default=TagType.COMMON)
    markdown = models.TextField(blank=True)
    html = models.TextField(blank=True)
    json = JSONField(default={})
    pinned = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(null=True, blank=True)
    cover = models.CharField(max_length=300, blank=True)

    children =  models.ManyToManyField('self', symmetrical=False, blank=True, related_name='parents')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:200] or '-'
        super().save(*args, **kwargs)

    @property
    def cover_url(self):
        if self.cover:
            return os.path.join(MEDIA_URL, self.cover)
        return os.path.join(STATIC_URL, 'images', 'no-image.png')

#-------------------------------------------------------------------------------
# Unmanaged join tables
#-------------------------------------------------------------------------------


class TagChildren(models.Model):

    parent  = models.ForeignKey(Tag, db_column='from_tag_id', related_name='+')
    child   = models.ForeignKey(Tag, db_column='to_tag_id', related_name='+')

    class Meta:
        db_table = 'tag_children'
        managed = False
        verbose_name_plural = 'Tag children'


#-------------------------------------------------------------------------------
# Signals
#-------------------------------------------------------------------------------

@receiver(post_delete, sender=Tag)
def tag_delete(instance, **kwargs):
    """
    Delete the physical files associated with this model
    """

    remove_media_file(instance.cover)
