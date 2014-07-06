from django.core.urlresolvers import reverse
from channel2.core.tests import BaseTestCase


class BlogViewTests(BaseTestCase):

    def test_blog_view_get(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog.html')


class BLogPostEditViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_blog_post_edit_view_get_no_id(self):
        response = self.client.get(reverse('blog.post.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog-post-edit.html')

    def test_blog_post_edit_view_post_no_id_invalid(self):
        response = self.client.post(reverse('blog.post.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog-post-edit.html')

    def test_blog_post_edit_view_post_no_id(self):
        pass
    def test_blog_post_edit_view_get(self):
        pass
    def test_blog_post_edit_view_post_invalid(self):
        pass
    def test_blog_post_edit_view_post(self):
        pass
