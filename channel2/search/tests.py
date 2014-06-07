from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase


class SearchViewTests(BaseTestCase):

    def test_search_view_get_empty(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')
