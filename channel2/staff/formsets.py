import os
import shutil

from django.forms import BaseFormSet
from django.forms.models import BaseModelFormSet

from channel2.core.utils import slugify, prepare_filepath
from channel2.settings import VIDEO_DIR, MEDIA_ROOT
from channel2.video.models import Video


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
