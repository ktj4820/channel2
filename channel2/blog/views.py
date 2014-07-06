from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from channel2.blog.forms import BlogPostForm
from channel2.blog.models import BlogPost
from channel2.core.views import ProtectedTemplateView, StaffTemplateView


class BlogView(ProtectedTemplateView):

    template_name = 'blog/blog.html'

    def get(self, request):
        return self.render_to_response({})


class BlogPostEditView(StaffTemplateView):

    template_name = 'blog/blog-post-edit.html'

    def get(self, request, id=None, slug=None):
        instance = id and get_object_or_404(BlogPost, id=id)
        return self.render_to_response({
            'form': BlogPostForm(instance=instance),
        })

    def post(self, request, id=None, slug=None):
        instance = id and get_object_or_404(BlogPost, id=id)
        form = BlogPostForm(instance=instance, data=request.POST)
        if form.is_valid():
            form.save(request)
            messages.success(request, _('The blog post has been successfully saved.'))
            return redirect('blog')

        return self.render_to_response({
            'form': form,
        })
