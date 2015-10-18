from channel2.core.tests import BaseTestCase
from channel2.tag.models import Tag


class TagModelTests(BaseTestCase):

    def test_tag_unique_slug(self):
        tag1 = Tag.objects.create(name='Test Tag 1')
        tag2 = Tag.objects.create(name='Test Tag 1?')
        tag3 = Tag.objects.create(name='Test Tag 1??')
        self.assertEqual(tag1.slug, 'test-tag-1')
        self.assertEqual(tag2.slug, 'test-tag-1-1')
        self.assertEqual(tag3.slug, 'test-tag-1-2')
