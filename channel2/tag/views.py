from channel2.core.views import ProtectedTemplateView


class TagListView(ProtectedTemplateView):

    template_name = 'tag/tag-list.html'

    def get(self, request):
        return self.render_to_response({})
