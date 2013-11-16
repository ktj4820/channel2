from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase


class FlatViewTests(BaseTestCase):

    def test_flat_help_view_get(self):
        response = self.client.get(reverse('flat.help'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flat/flat-help.html')
