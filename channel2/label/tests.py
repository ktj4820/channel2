from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase
from channel2.label.models import Label


class LabelListViewTests(BaseTestCase):

    def test_label_list_view_get(self):
        response = self.client.get(reverse('label.list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/label-list.html')


class LabelViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.label = self.label_list[0]

    def test_label_view_get(self):
        response = self.client.get(reverse('label', args=[self.label.id, self.label.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/label.html')


class LabelEditViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.label = self.label_list[0]

    def test_label_edit_view_get(self):
        response = self.client.get(reverse('label.edit', args=[self.label.id, self.label.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/label-edit.html')

    def test_label_edit_view_post_invalid(self):
        response = self.client.post(reverse('label.edit', args=[self.label.id, self.label.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/label-edit.html')

    def test_label_edit_view_post(self):
        response = self.client.post(reverse('label.edit', args=[self.label.id, self.label.slug]), {
            'name': 'Updated Name',
            'markdown': 'Sample markdown',
            'html': 'Sample HTML',
        })

        label = Label.objects.get(id=self.label.id)
        self.assertRedirects(response, reverse('label', args=[label.id, label.slug]))
        self.assertEqual(label.name, 'Updated Name')
        self.assertEqual(label.markdown, 'Sample markdown')
        self.assertEqual(label.html, 'Sample HTML')
