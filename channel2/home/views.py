from channel2.core.views import ProtectedTemplateView
from channel2.tag.enums import TagType
from channel2.tag.models import Tag


class HomeView(ProtectedTemplateView):

    template_name = 'home/home.html'

    def get(self, request):
        new_list = Tag.objects.filter(type=TagType.ANIME).prefetch_related('children').order_by('-created_on')[:10]
        for tag in new_list:
            tag.children_list = sorted(tag.children.all(), key=lambda t: t.name)
        return self.render_to_response({
            'new_list': new_list,
        })
