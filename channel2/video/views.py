from channel2.core.views import ProtectedTemplateView


class VideoListView(ProtectedTemplateView):

    template_name = 'video/video-list.html'

    def get(self, request):
        return self.render_to_response({})
