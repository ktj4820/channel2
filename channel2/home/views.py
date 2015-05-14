from channel2.core.views import ProtectedTemplateView
from channel2.tag.enums import TagType
from channel2.tag.models import Tag
from channel2.video.models import VideoLink


class HomeView(ProtectedTemplateView):

    template_name = 'home/home.html'

    def get(self, request):
        recent_tag_id_list = VideoLink.objects.filter(created_by=request.user).order_by('-created_on').values_list('video__tag_id', flat=True)[:25]
        tag_id_list = []
        for tid in recent_tag_id_list:
            if tid not in tag_id_list: tag_id_list.append(tid)
        tag_list = Tag.objects.filter(id__in=tag_id_list)
        tag_dict = {t.id: t for t in tag_list}
        recent_list = [tag_dict[tid] for tid in tag_id_list]

        new_list = Tag.objects.filter(type=TagType.ANIME).prefetch_related('children').order_by('-created_on')[:10]
        for tag in new_list:
            tag.children_list = sorted(tag.children.all(), key=lambda t: t.name)
        return self.render_to_response({
            'new_list': new_list,
            'recent_list': recent_list[:5],
        })
