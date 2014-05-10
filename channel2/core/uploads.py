import os


def video_file_upload_to(instance, filename):
    filename = '{}.mp4'.format(instance.slug)
    dir = instance.label.slug if instance.label else 'unknown'
    return os.sep.join(['video', dir, filename])


def video_cover_upload_to(instance, filename):
    filename = '{}.jpg'.format(instance.slug)
    dir = instance.label.slug if instance.label else 'unknown'
    return os.sep.join(['cover', dir, filename])
