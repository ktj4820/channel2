from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
import os

from channel2.account.models import User
from channel2.core.utils import slugify, remove_media_file
from channel2.settings import MEDIA_ROOT, MEDIA_URL
from channel2.tag.models import Tag


class Video(models.Model):

    file = models.CharField(max_length=300, unique=True)
    name = models.CharField(max_length=200)
    episode = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200)
    views = models.IntegerField(default=0)
    cover = models.CharField(max_length=300, blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'video'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:200] or '-'
        super().save(*args, **kwargs)

    @property
    def filepath(self):
        return os.path.join(MEDIA_ROOT, self.file)

    @property
    def url(self):
        return os.path.join(MEDIA_URL, self.file)


class VideoLink(models.Model):

    video = models.ForeignKey(Video)
    key = models.CharField(max_length=64, unique=True)
    ip_address = models.CharField(max_length=200)

    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='+')

    class Meta:
        db_table = 'video_link'


#-------------------------------------------------------------------------------
# Signals
#-------------------------------------------------------------------------------

@receiver(post_delete, sender=Video)
def video_delete(instance, **kwargs):
    """
    Delete the physical files associated with this model
    """

    remove_media_file(instance.file)
    remove_media_file(instance.cover)
