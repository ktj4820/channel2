from django.db.models.aggregates import Count
from channel2.core.views import ProtectedTemplateView
from channel2.tag.models import Tag


class TagListView(ProtectedTemplateView):

    template_name = 'tag/tag-list.html'

    def get(self, request):
        tag_list = Tag.objects.order_by('slug').annotate(count=Count('video')).prefetch_related('tags')
        return self.render_to_response({
            'tag_list': tag_list,
        })


class TagView(ProtectedTemplateView):

    template_name = 'tag/tag.html'

    def get(self, request, id, slug):
        return self.render_to_response({})
