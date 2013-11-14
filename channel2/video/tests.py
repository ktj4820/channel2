import os
import tempfile
from django.core.files.base import File
from channel2.core.tests import BaseTestCase
from channel2.video.models import Video


class VideoModelTests(BaseTestCase):

    def test_video_save_slugify(self):
        video = Video.objects.create(name='Test Episode 01')
        self.assertEqual(video.slug, 'test-episode-01')

    def test_video_delete(self):
        file = tempfile.NamedTemporaryFile(suffix='.mp4')

        video = Video.objects.create(name='Test Video')
        video.file.save(file.name, File(file))
        self.assertTrue(os.path.exists(video.file.path))

        video.delete()
        self.assertFalse(os.path.exists(video.file.path))
