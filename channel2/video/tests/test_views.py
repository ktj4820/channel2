from urllib.parse import urlsplit
import binascii
import os

from django.core.urlresolvers import reverse
from django.utils import timezone

from channel2.core.tests import BaseTestCase
from channel2.core.utils import prepare_filepath
from channel2.settings import VIDEO_LINK_EXPIRE, MEDIA_ROOT
from channel2.video.models import Video, VideoLink
from channel2.video.views import VideoLinkView


class VideoViewTests(BaseTestCase):

    def setUp(self):
        super(VideoViewTests, self).setUp()

    def test_video_view_get(self):
        video = Video.objects.all()[0]
        response = self.client.get(reverse('video', args=[video.id, video.slug]))

        link = VideoLink.objects.get(video=video)
        redirect_location = reverse('video.link', args=[link.key, video.slug])
        self.assertRedirects(response, redirect_location, target_status_code=302)
        self.assertEqual(video.views+1, Video.objects.get(id=video.id).views)

        response = self.client.get(reverse('video', args=[video.id, video.slug]))
        self.assertRedirects(response, redirect_location, target_status_code=302)
        self.assertEqual(video.views+1, Video.objects.get(id=video.id).views)


class VideoLinkViewTests(BaseTestCase):

    def setUp(self):
        super(VideoLinkViewTests, self).setUp()

        self.video = Video.objects.all()[0]

        filepath = os.path.join(MEDIA_ROOT, self.video.file)
        prepare_filepath(filepath)
        open(filepath, 'a').close()

        self.link = VideoLink.objects.create(
            video=self.video,
            key=binascii.hexlify(os.urandom(32)),
            ip_address='127.0.0.1',
            created_by=self.user,
        )

    def tearDown(self):
        self.video.delete()

    def test_video_link_view_get_file_missing(self):
        self.video.file = ''
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
        self.assertEqual(self.video.url, actual_path)


class VideoHistoryViewTests(BaseTestCase):

    def test_video_history_view_get(self):
        response = self.client.get(reverse('video.history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video/video-history.html')
