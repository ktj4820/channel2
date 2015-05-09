import os

from channel2.core.tests import BaseTestCase
from channel2.settings import MEDIA_ROOT
from channel2.tag.models import Tag
from channel2.video.models import Video


class VideoModelTests(BaseTestCase):

    def test_video_save_slugify(self):
        video = Video.objects.create(name='Test Episode 01', tag=Tag.objects.all()[0])
        self.assertEqual(video.slug, 'test-episode-01')

    def test_video_delete(self):
        file = 'test-video-01.mp4'
        file_path = os.path.join(MEDIA_ROOT, file)

        open(file_path, 'a').close()
        self.assertTrue(os.path.exists(file_path))

        video = Video.objects.create(
            name='Test Video',
            tag=Tag.objects.all()[0],
            file=file,
        )

        video.delete()
        self.assertFalse(os.path.exists(file_path))
