from django.core.urlresolvers import reverse

from channel2.core.tests import BaseTestCase
from channel2.tag.models import Tag


class TagListViewTests(BaseTestCase):

    def test_tag_list_view_get(self):
        response = self.client.get(reverse('tag.list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag/tag-list.html')


class TagListAnimeViewTests(BaseTestCase):

    def test_tag_list_anime_view_get(self):
        response = self.client.get(reverse('tag.list.anime'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag/tag-list.html')


class TagViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.get(name='Action')

    def test_tag_view_get(self):
        response = self.client.get(reverse('tag', args=[self.tag.id, self.tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag/tag.html')


class TagRandomViewTests(BaseTestCase):

    def test_tag_random_view_get(self):
        response = self.client.get(reverse('tag.random'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/tag/' in response['location'])


class TagCurrentViewTests(BaseTestCase):

    def test_tag_current_view_get(self):
        response = self.client.get(reverse('tag.current'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag/tag-current.html')
