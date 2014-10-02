from django.db.models.aggregates import Count

from channel2.core.views import ProtectedTemplateView
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
        recent_tag_list = [tag_dict[tid] for tid in tag_id_list]
        new_tag_list = Tag.objects.annotate(count=Count('video')).filter(count__gt=0).order_by('-created_on')[:10]
        return self.render_to_response({
            'recent_tag_list': recent_tag_list,
            'new_tag_list': new_tag_list,
        })
