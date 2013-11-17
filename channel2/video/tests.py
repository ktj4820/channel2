import binascii
import os
import tempfile
from urllib.parse import urlsplit
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
        file = tempfile.NamedTemporaryFile(suffix='.mp4')

        video = Video.objects.create(name='Test Video')
        video.file.save(file.name, File(file))
        self.assertTrue(os.path.exists(video.file.path))

        video.delete()
        self.assertFalse(os.path.exists(video.file.path))


class VideoViewTests(BaseTestCase):

    def setUp(self):
        super(VideoViewTests, self).setUp()

    def test_video_list_view_get_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('video.list'))
        self.assertRedirects(response, '{}?next={}'.format(reverse('account.login'), reverse('video.list')))

    def test_video_list_view_get(self):
        response = self.client.get(reverse('video.list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video/video-list.html')

    def test_video_view_get(self):
        video = Video.objects.all()[0]
        response = self.client.get(reverse('video', args=[video.id, video.slug]))
        link = VideoLink.objects.get(video=video)
        self.assertRedirects(response, reverse('video.link', args=[link.key, video.slug]))
        self.assertEqual(video.views+1, Video.objects.get(id=video.id).views)


class VideoLinkViewTests(BaseTestCase):

    def setUp(self):
        super(VideoLinkViewTests, self).setUp()

        self.video = Video.objects.all()[0]
        file = tempfile.NamedTemporaryFile(suffix='.mp4')
        self.video.file.save(file.name, File(file))

        self.link = VideoLink.objects.create(
            video=self.video,
            key=binascii.hexlify(os.urandom(32)),
            ip_address='127.0.0.1',
            created_by=self.user,
        )

    def tearDown(self):
        self.video.delete()

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
