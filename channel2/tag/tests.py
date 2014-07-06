from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase
from channel2.tag.forms import TagForm
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


class TagEditViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.create(name='tag1')

    def test_tag_edit_view_get(self):
        response = self.client.get(reverse('tag.edit', args=[self.tag.id, self.tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag/tag-edit.html')

    def test_tag_edit_view_post_invalid(self):
        response = self.client.post(reverse('tag.edit', args=[self.tag.id, self.tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag/tag-edit.html')

    def test_tag_edit_view_post(self):
        response = self.client.post(reverse('tag.edit', args=[self.tag.id, self.tag.slug]), {
            'name': 'Updated Name',
            'markdown': 'Sample markdown',
        })

        tag = Tag.objects.get(id=self.tag.id)
        self.assertRedirects(response, reverse('tag', args=[tag.id, tag.slug]))
        self.assertEqual(tag.name, 'Updated Name')
        self.assertEqual(tag.markdown, 'Sample markdown')
        self.assertEqual(tag.html, '<p>Sample markdown</p>')


class TagFormTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.create(name='Test Tag')

    def test_tag_form_children(self):
        tag1 = Tag.objects.create(name='tag1')

        form = TagForm(instance=self.tag, data={
            'name': 'Test Tag',
            'children': 'tag1, tag2',
        })
        self.assertTrue(form.is_valid())
        tag = form.save()

        tag2 = Tag.objects.get(name='tag2')

        tag_children_list = tag.children.all()
        self.assertTrue(tag1 in tag_children_list)
        self.assertTrue(tag2 in tag_children_list)


class TagModelTests(BaseTestCase):

    def test_tag_tags_m2m(self):
        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2')

        tag1.children.add(tag2)

        self.assertTrue(tag2 in tag1.children.all())
        self.assertFalse(tag1 in tag2.children.all())
