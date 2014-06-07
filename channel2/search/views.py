from channel2.core.utils import paginate
from channel2.core.views import ProtectedTemplateView
from channel2.search.forms import VideoSearchForm
from channel2.video.models import Video


class SearchView(ProtectedTemplateView):

    template_name = 'search/search.html'
    page_size = 12

    def get(self, request):
        form = VideoSearchForm(data=request.GET)
        page = paginate(form.search(), self.page_size, request.GET.get('p'))
        video_list = Video.objects.filter(id__in=[obj.pk for obj in page.object_list])
        return self.render_to_response({
            'video_list': video_list,
            'page': page,
        })
