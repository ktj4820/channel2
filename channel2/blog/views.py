from channel2.core.views import ProtectedTemplateView, StaffTemplateView


class BlogView(ProtectedTemplateView):

    template_name = 'blog/blog.html'

    def get(self, request):
        return self.render_to_response({})


class BlogPostEditView(StaffTemplateView):

    template_name = 'blog/blog-post-edit.html'

    def get(self, request, id=None, slug=None):
        return self.render_to_response({})

    def post(self, request, id=None, slug=None):
        return self.render_to_response({})
