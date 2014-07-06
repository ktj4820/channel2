from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase


class BlogViewTests(BaseTestCase):

    def test_blog_view_get(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog.html')
