from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase


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
