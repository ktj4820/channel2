from django.core.urlresolvers import reverse

from channel2.core.tests import BaseTestCase
from channel2.tag.forms import TagForm
from channel2.tag.models import Tag
from channel2.video.models import Video


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


class TagCreateViewTests(BaseTestCase):

    def test_tag_create_view_get(self):
        response = self.client.get(reverse('tag.create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag/tag-edit.html')

    def test_tag_create_view_post_invalid(self):
        response = self.client.post(reverse('tag.create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag/tag-edit.html')

    def test_tag_create_view_post(self):
        response = self.client.post(reverse('tag.create'), {
            'name': 'New Tag',
            'markdown': 'Some markdown for the new tag.',
        })
        tag = Tag.objects.get(name='New Tag')
        self.assertRedirects(response, reverse('tag.edit', args=[tag.id, tag.slug]))

        self.assertEqual(tag.markdown, 'Some markdown for the new tag.')
        self.assertEqual(tag.html, '<p>Some markdown for the new tag.</p>')
        self.assertFalse(tag.pinned)
        self.assertEqual(tag.order, None)


class TagEditViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.all()[0]

    def test_tag_edit_view_get_not_staff(self):
        self.user.is_staff = False
        self.user.save()

        response = self.client.get(reverse('tag.video', args=[self.tag.id, self.tag.slug]))
        self.assertEqual(response.status_code, 404)

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
            'name': 'New Tag Name',
            'markdown': 'Some new markdown for the tag',
        })
        tag = Tag.objects.get(id=self.tag.id)
        self.assertRedirects(response, reverse('tag.edit', args=[tag.id, tag.slug]))

        self.assertEqual(tag.name, 'New Tag Name')
        self.assertEqual(tag.markdown, 'Some new markdown for the tag')
        self.assertEqual(tag.pinned, False)
        self.assertEqual(tag.order, None)
        self.assertEqual(tag.html, '<p>Some new markdown for the tag</p>')


class TagDeleteViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.all()[0]
        
    def test_tag_delete_view_get(self):
        response = self.client.get(reverse('tag.delete', args=[self.tag.id, self.tag.slug]))
        self.assertEqual(response.status_code, 405)
        
    def test_tag_delete_view_post(self):
        response = self.client.post(reverse('tag.delete', args=[self.tag.id, self.tag.slug]))
        self.assertRedirects(response, reverse('tag.list'))
        self.assertFalse(Tag.objects.filter(id=self.tag.id).exists())

    def test_tag_delete_view_post_with_videos(self):
        video = Video.objects.all()[0]
        video.tag = self.tag
        video.save()

        response = self.client.post(reverse('tag.delete', args=[self.tag.id, self.tag.slug]))
        self.assertRedirects(response, reverse('tag.list'))
        self.assertFalse(Tag.objects.filter(id=self.tag.id).exists())
        self.assertFalse(Video.objects.filter(id=video.id).exists())


class TagAutocompleteJsonViewTests(BaseTestCase):

    def test_tag_autocomplete_json_view_get(self):
        tag_list = Tag.objects.all().order_by('slug').values_list('name', flat=True)
        tag_list = ['"{}"'.format(name) for name in tag_list]
        response = self.client.get(reverse('tag.autocomplete.json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[{}]'.format(', '.join(tag_list)).encode('utf-8'))


class TagVideoViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.tag = Tag.objects.all()[0]

    def test_tag_video_view_get_not_staff(self):
        self.user.is_staff = False
        self.user.save()

        response = self.client.get(reverse('tag.video', args=[self.tag.id, self.tag.slug]))
        self.assertEqual(response.status_code, 404)

    def test_tag_video_view_get(self):
        response = self.client.get(reverse('tag.video', args=[self.tag.id, self.tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tag/tag-video.html')

    def test_tag_video_view_post(self):
        response = self.client.post(reverse('tag.video', args=[self.tag.id, self.tag.slug]), {
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '100',
        })
        self.assertRedirects(response, reverse('tag.video', args=[self.tag.id, self.tag.slug]))


class TagFormTests(BaseTestCase):

    def test_tag_form_create(self):
        form = TagForm(user=self.user, data={
            'name': 'New Tag',
            'markdown': 'Some markdown for the new tag.',
        })
        self.assertTrue(form.is_valid(), form.errors)
        tag = form.save()

        self.assertEqual(tag.name, 'New Tag')
        self.assertEqual(tag.updated_by, self.user)
        self.assertEqual(tag.created_by, self.user)
        self.assertEqual(tag.markdown, 'Some markdown for the new tag.')
        self.assertEqual(tag.html, '<p>Some markdown for the new tag.</p>')

    def test_tag_form_create_name_with_comma(self):
        form = TagForm(user=self.user, data={
            'name': 'New Tag, with comma',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [TagForm.error_messages['name.has.comma']])

    def test_tag_form_create_children_not_exists(self):
        form = TagForm(user=self.user, data={
            'name': 'New Tag',
            'children': 'Invalid Tag',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['children'], [TagForm.error_messages['tag.not.found'].format('Invalid Tag')])

    def test_tag_form_create_children(self):
        form = TagForm(user=self.user, data={
            'name': 'New Tag',
            'children': ', '.join([tag.name for tag in Tag.objects.all()]),
        })
        self.assertTrue(form.is_valid())
        tag = form.save()
        self.assertEqual(set(tag.children.all()), set(Tag.objects.all().exclude(id=tag.id)))

        form = TagForm(user=self.user, instance=tag, data={
            'name': 'New Tag',
            'children': '',
        })
        self.assertTrue(form.is_valid())
        tag = form.save()
        self.assertEqual(set(tag.children.all()), set())
