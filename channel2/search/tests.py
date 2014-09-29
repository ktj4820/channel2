from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase
from channel2.tag.models import Tag


class SearchViewTests(BaseTestCase):

    def test_search_view_get(self):
        tag = Tag.objects.create(name='Test Tag', slug='test-tag')
        response = self.client.get(reverse('search'), {
            'q': tag.name,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')

    def test_search_view_get_empty(self):
        response = self.client.get(reverse('search'), {})
        self.assertRedirects(response, reverse('home'))

    def test_search_view_get_no_results(self):
        response = self.client.get(reverse('search'), {
            'q': 'this is a simple phrase',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/search.html')
