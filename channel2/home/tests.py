from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase


class HomeViewTests(BaseTestCase):

    def test_home_view_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_home_view_get_anonymous(self):
        self.client.logout()

        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '{}?next={}'.format(reverse('account.login'), reverse('home')))
