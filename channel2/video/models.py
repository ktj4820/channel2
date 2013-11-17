import os, subprocess
from django.core.files.base import File
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from channel2.account.models import User
from channel2.core.utils import slugify
from channel2.label.models import Label
from channel2.settings import FFMPEG_PATH


def video_file_upload_to(instance, filename):
    filename = '{}.mp4'.format(instance.slug)
    dir = instance.label.slug if instance.label else 'unknown'
    return os.sep.join(['video', dir, filename])


def video_cover_upload_to(instance, filename):
    filename = '{}.jpg'.format(instance.slug)
    dir = instance.label.slug if instance.label else 'unknown'
    return os.sep.join(['cover', dir, filename])


class Video(models.Model):

    file            = models.FileField(upload_to=video_file_upload_to, null=True, blank=True)

    name            = models.CharField(max_length=100)
    slug            = models.SlugField(max_length=100)
    views           = models.IntegerField(default=0)
    label           = models.ForeignKey(Label, null=True, blank=True, on_delete=models.SET_NULL)
    cover           = models.FileField(upload_to=video_cover_upload_to, null=True, blank=True)

    created_on      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'video'

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:100] or '-'
        super().save(*args, **kwargs)

        if not self.cover:
            self.generate_cover()

    def generate_cover(self):
        """
        generate a cover using the ffmpeg command:
        ffmpeg -ss 00:00:05 -t 1 -i <input_file.file> -s 960x540 -f image2 <output.jpg>
        """

        if self.file and FFMPEG_PATH:
            cover_path = '/tmp/{}.jpg'.format(self.slug)

            subprocess.call([
                FFMPEG_PATH, '-ss', '00:00:05', '-t', '1',
                '-i', self.file.path,
                '-s', '960x540', '-f', 'image2', cover_path
            ])

            if os.path.exists(cover_path):
                self.cover.delete()
                self.cover.save('', File(open(cover_path)), save=True)


class VideoLink(models.Model):

    video           = models.ForeignKey(Video)
    key             = models.CharField(max_length=64, db_index=True)
    ip_address      = models.CharField(max_length=64)

    created_on      = models.DateTimeField(auto_now_add=True)
    created_by      = models.ForeignKey(User, related_name='+')

    class Meta:
        db_table = 'video_link'


@receiver(post_delete, sender=Video)
def video_delete(instance, **kwargs):
    """
    delete the physical files associated with this model
    """

    file = instance.file
    if file: file.storage.delete(file.path)

    cover = instance.cover
    if cover: cover.storage.delete(cover.path)
