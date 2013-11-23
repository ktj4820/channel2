from django.db.models.query_utils import Q
from channel2.core.utils import paginate
from channel2.core.views import ProtectedTemplateView
from channel2.video.models import Video


class SearchView(ProtectedTemplateView):

    template_name = 'search/search.html'
    page_size = 12

    def get_video_list(self):
        query = self.request.GET.get('q')
        if query:
            video_list = Video.objects.filter(Q(name__icontains=query) | Q(label__name__icontains=query))
        else:
            video_list = []
        return video_list

    def get(self, request):
        video_list = self.get_video_list()
        video_list = paginate(video_list, self.page_size, request.GET.get('p'))
        return self.render_to_response({
            'video_list': video_list,
        })
