from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase


class VideoListViewTests(BaseTestCase):

    def test_video_list_view_get(self):
        response = self.client.get(reverse('video.list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video/video-list.html')
