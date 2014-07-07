from django.core.urlresolvers import reverse
from channel2.blog.models import BlogPost
from channel2.core.tests import BaseTestCase


class BlogViewTests(BaseTestCase):

    def test_blog_view_get(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog.html')


class BLogPostEditViewTests(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.blog_post = BlogPost.objects.create(
            title='Test Post Title',
            markdown='Test post markdown content.',
            html='<p>Test post markdown content.</p>',
            created_by=self.user,
        )

    def test_blog_post_edit_view_get_no_id(self):
        response = self.client.get(reverse('blog.post.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog-post-edit.html')

    def test_blog_post_edit_view_post_no_id_invalid(self):
        response = self.client.post(reverse('blog.post.add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog-post-edit.html')

    def test_blog_post_edit_view_post_no_id(self):
        response = self.client.post(reverse('blog.post.add'), {
            'title': 'This is a sample blog post title.',
            'markdown': 'This is some sample markdown for the blog post',
        })
        self.assertRedirects(response, reverse('blog'))

        blog_post = BlogPost.objects.get(title='This is a sample blog post title.')
        self.assertEqual(blog_post.markdown, 'This is some sample markdown for the blog post')
        self.assertEqual(blog_post.html, '<p>This is some sample markdown for the blog post</p>')

    def test_blog_post_edit_view_get(self):
        response = self.client.get(reverse('blog.post.edit', args=[self.blog_post.id, self.blog_post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog-post-edit.html')

    def test_blog_post_edit_view_post_invalid(self):
        response = self.client.post(reverse('blog.post.edit', args=[self.blog_post.id, self.blog_post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog-post-edit.html')

    def test_blog_post_edit_view_post(self):
        response = self.client.post(reverse('blog.post.edit', args=[self.blog_post.id, self.blog_post.slug]), {
            'title': 'This is a sample blog post title.',
            'markdown': 'This is some sample markdown for the blog post',
        })
        self.assertRedirects(response, reverse('blog'))

        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        self.assertEqual(blog_post.markdown, 'This is some sample markdown for the blog post')
        self.assertEqual(blog_post.html, '<p>This is some sample markdown for the blog post</p>')

    def test_blog_post_edit_view_post_delete(self):
        response = self.client.post(reverse('blog.post.edit', args=[self.blog_post.id, self.blog_post.slug]), {
            'action': 'delete',
        })
        self.assertRedirects(response, reverse('blog'))
        self.assertFalse(BlogPost.objects.filter(id=self.blog_post.id).exists())
