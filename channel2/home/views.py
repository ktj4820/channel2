from channel2.core.views import ProtectedTemplateView
from channel2.tag.models import Tag


class HomeView(ProtectedTemplateView):

    template_name = 'home/home.html'

    def get(self, request):
        tag_list = Tag.objects.order_by('-sort_date')[:10]
        return self.render_to_response({
            'tag_list': tag_list,
        })
