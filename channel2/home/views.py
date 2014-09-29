from channel2.core.views import ProtectedTemplateView


class HomeView(ProtectedTemplateView):

    template_name = 'home/home.html'

    def get(self, request):
        return self.render_to_response({})
