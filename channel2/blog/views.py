from channel2.core.views import ProtectedTemplateView


class BlogView(ProtectedTemplateView):

    template_name = 'blog/blog.html'

    def get(self, request):
        return self.render_to_response({})
