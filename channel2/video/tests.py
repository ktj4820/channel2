import tempfile
import binascii
from urllib.parse import urlsplit
import os

from django.core.files.base import File
from django.core.urlresolvers import reverse
from django.utils import timezone

from channel2.core.tests import BaseTestCase
from channel2.settings import VIDEO_LINK_EXPIRE
from channel2.video.models import Video, VideoLink
from channel2.video.views import VideoLinkView


class VideoModelTests(BaseTestCase):

    def test_video_save_slugify(self):
        video = Video.objects.create(name='Test Episode 01')
        self.assertEqual(video.slug, 'test-episode-01')

    def test_video_delete(self):
        file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)

        video = Video.objects.create(name='Test Video')
        video.file.save(file.name, File(file))
        self.assertTrue(os.path.exists(video.file.path))

        video.delete()
        self.assertFalse(os.path.exists(video.file.path))


class VideoLinkViewTests(BaseTestCase):

    def setUp(self):
        super(VideoLinkViewTests, self).setUp()

        self.video = Video.objects.all()[0]
        self.file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
        self.video.file.save(self.file.name, File(self.file))

        self.link = VideoLink.objects.create(
            video=self.video,
            key=binascii.hexlify(os.urandom(32)),
            ip_address='127.0.0.1',
            created_by=self.user,
        )

    def tearDown(self):
        self.video.delete()
        os.remove(self.file.name)

    def test_video_link_view_get_file_missing(self):
        self.video.file.delete()
        self.video.file = None
        self.video.save()

        response = self.client.get(reverse('video.link', args=[self.link.key, self.video.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video/video-unavailable.html')
        self.assertTrue(VideoLinkView.messages['file_missing'] in str(response.content))

    def test_video_link_view_get_link_expired(self):
        self.link.created_on = timezone.now() - timezone.timedelta(seconds=VIDEO_LINK_EXPIRE+1)
        self.link.save()

        response = self.client.get(reverse('video.link', args=[self.link.key, self.video.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video/video-unavailable.html')
        self.assertTrue(VideoLinkView.messages['link_expired'] in str(response.content))

    def test_video_link_view_get_ip_address_mismatch(self):
        self.link.ip_address = 'other ip'
        self.link.save()

        response = self.client.get(reverse('video.link', args=[self.link.key, self.video.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video/video-unavailable.html')
        self.assertTrue(VideoLinkView.messages['ip_address_mistmatch'] in str(response.content))

    def test_video_link_view_get(self):
        response = self.client.get(reverse('video.link', args=[self.link.key, self.video.slug]))
        self.assertEqual(response.status_code, 302)

        actual_path = urlsplit(response['location'])[2]
        self.assertEqual(self.video.file.url, actual_path)


class VideoHistoryViewTests(BaseTestCase):

    def test_video_history_view_get(self):
        for video in Video.objects.all():
            VideoLink.objects.create(video=video, key='1'*64, ip_address='127.0.0.1', created_by=self.user)

        response = self.client.get(reverse('video.history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video/video-history.html')


class VideoHistoryDeleteViewTests(BaseTestCase):

    def test_video_history_delete_view_get(self):
        response = self.client.get(reverse('video.history.delete'))
        self.assertEqual(response.status_code, 405)

    def test_video_history_delete_view_post(self):
        video_list = Video.objects.all()
        for video in video_list:
            VideoLink.objects.create(video=video, key='1'*64, ip_address='127.0.0.1', created_by=self.user)
        self.assertEqual(VideoLink.objects.filter(created_by=self.user).count(), len(video_list))

        response = self.client.post(reverse('video.history.delete'))
        self.assertRedirects(response, reverse('video.history'))
        self.assertEqual(VideoLink.objects.filter(created_by=self.user).count(), 0)
