from channel2.core.utils import paginate
from channel2.core.views import ProtectedTemplateView
from channel2.video.models import Video


class VideoListView(ProtectedTemplateView):

    template_name = 'video/video-list.html'
    page_size = 12

    def get(self, request):
        video_list = Video.objects.order_by('-created_on')
        video_list = paginate(video_list, self.page_size, request.GET.get('p'))
        return self.render_to_response({
            'video_list': video_list,
        })
