from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404

from channel2.core.views import ProtectedTemplateView
from channel2.tag.models import Tag


class TagListView(ProtectedTemplateView):

    template_name = 'tag/tag-list.html'

    def get(self, request):
        tag_list = Tag.objects.order_by('slug').annotate(count=Count('video'))
        return self.render_to_response({
            'tag_list': tag_list,
        })


class TagView(ProtectedTemplateView):

    template_name = 'tag/tag.html'

    def get(self, request, id, slug):
        tag = get_object_or_404(Tag, id=id)
        tag_children_list = tag.children.all()

        return self.render_to_response({
            'tag': tag,
            'tag_children_list': tag_children_list,
        })
