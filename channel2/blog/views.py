from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from channel2.blog.forms import BlogPostForm
from channel2.blog.models import BlogPost
from channel2.core.utils import paginate
from channel2.core.views import ProtectedTemplateView, StaffTemplateView


class BlogView(ProtectedTemplateView):

    page_size = 10
    template_name = 'blog/blog.html'

    def get(self, request):
        blog_post_list = BlogPost.objects.order_by('-created_on').select_related('created_by')
        blog_post_list = paginate(blog_post_list, self.page_size, request.GET.get('p'))
        return self.render_to_response({
            'blog_post_list': blog_post_list,
        })


class BlogPostEditView(StaffTemplateView):

    template_name = 'blog/blog-post-edit.html'

    def get(self, request, id=None, slug=None):
        blog_post = id and get_object_or_404(BlogPost, id=id)
        return self.render_to_response({
            'blog_post': blog_post,
            'form': BlogPostForm(instance=blog_post),
        })

    def post(self, request, id=None, slug=None):
        blog_post = id and get_object_or_404(BlogPost, id=id)
        form = BlogPostForm(instance=blog_post, data=request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, _('The blog post has been successfully saved.'))
            return redirect('blog')

        return self.render_to_response({
            'blog_post': blog_post,
            'form': form,
        })
