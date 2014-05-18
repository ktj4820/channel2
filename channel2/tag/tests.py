from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase
from channel2.tag.models import Tag


class TagListViewTests(BaseTestCase):

    def test_tag_list_view_get(self):
        response = self.client.get(reverse('tag.list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag/tag-list.html')


class TagViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.pinned_tag = Tag.objects.filter(pinned=True)[0]
        self.tag = Tag.objects.filter(pinned=False)[0]

    def test_tag_view_get(self):
        response = self.client.get(reverse('tag', args=[self.tag.id, self.tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag/tag.html')


class TagModelTests(BaseTestCase):

    def test_tag_tags_m2m(self):
        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2')

        tag1.children.add(tag2)

        self.assertTrue(tag2 in tag1.children.all())
        self.assertFalse(tag1 in tag2.children.all())
