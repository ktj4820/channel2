from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase, TestRequest
from channel2.search.views import SearchView


class SearchViewTests(BaseTestCase):

    def test_search_view_get_empty(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')

    def test_search_view_get_video_list_empty(self):
        view = SearchView()
        view.request = TestRequest(GET={})
        video_list = view.get_video_list()
        self.assertFalse(video_list)

    def test_search_view_get_video_list(self):
        view = SearchView()
        view.request = TestRequest(GET={'q': 'Another'})
        video_list = view.get_video_list()
        for video in video_list:
            self.assertTrue('Another' in video.name, '"Another" not found in video name')
