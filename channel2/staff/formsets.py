import os
import shutil

from django import forms
from django.forms import BaseFormSet
from django.forms.models import BaseModelFormSet

from channel2.core.utils import slugify, prepare_filepath
from channel2.settings import VIDEO_DIR, MEDIA_ROOT
from channel2.tag.models import Tag
from channel2.video.models import Video


class StaffVideoFormSet(BaseFormSet):

    def clean(self):
        # generate filepath for each form
        data_list = self.cleaned_data
        for data in data_list:
            name = data['name']
            data['tag'] = tag = Tag.objects.get_or_create(name=data['tag'])[0]
            data['filepath'] = os.path.join('video', tag.slug, '{}.mp4'.format(slugify(name)))

        # ensure that all filepaths are unique
        filepath_list = [d['filepath'] for d in data_list]
        if len(filepath_list) > len(set(filepath_list)):
            raise forms.ValidationError('Non-unique filepaths were generated from video names.')

        # ensure that no filepaths already exists in the database
        if Video.objects.filter(file__in=filepath_list).exists():
            raise forms.ValidationError('Auto generated filepaths already exists in the database.')

        return data_list

    def save(self):
        for form in self.ordered_forms:
            data = form.cleaned_data
            if not data.get('selected'):
                continue

            name = data['name']
            tag = data['tag']
            new_filepath = data['filepath']

            # move the file in filepath to the correct location
            cur_filepath_abs = os.path.join(VIDEO_DIR, data.get('filename'))
            new_filepath_abs = os.path.join(MEDIA_ROOT, new_filepath)
            prepare_filepath(new_filepath_abs)
            shutil.move(cur_filepath_abs, new_filepath_abs)

            Video.objects.create(
                file=new_filepath,
                name=name,
                episode=data.get('episode', ''),
                tag=tag,
            )


class StaffTagVideoFormSet(BaseFormSet):

    def save(self, tag):
        for form in self.ordered_forms:
            data = form.cleaned_data
            if not data.get('selected'):
                continue

            name = data['name']

            # move the file in filepath to the correct location
            cur_filepath_abs = os.path.join(VIDEO_DIR, data.get('filename'))

            new_filepath = os.path.join('video', tag.slug, '{}.mp4'.format(slugify(name)))
            new_filepath_abs = os.path.join(MEDIA_ROOT, new_filepath)
            prepare_filepath(new_filepath_abs)
            shutil.move(cur_filepath_abs, new_filepath_abs)

            Video.objects.create(
                file=new_filepath,
                name=name,
                episode=data.get('episode', ''),
                tag=tag,
            )


class StaffTagPinnedFormSet(BaseModelFormSet):

    def save(self):
        for form in self.deleted_forms:
            tag = form.instance
            tag.pinned = False
            tag.order = None
            tag.save()

        for i, form in enumerate(self.ordered_forms, start=1):
            tag = form.instance
            tag.order = i
            tag.save()
