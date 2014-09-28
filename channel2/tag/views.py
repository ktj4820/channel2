from collections import defaultdict

from django.shortcuts import get_object_or_404

from channel2.core.views import ProtectedTemplateView
from channel2.tag.models import Tag, TagChildren


class TagView(ProtectedTemplateView):

    template_name = 'tag/tag.html'

    def get(self, request, id, slug):
        tag = get_object_or_404(Tag, id=id)
        tag_children_list = tag.children.order_by('slug')
        tag_parent_list = tag.parents.order_by('slug')

        # get the children list for each parent, but exclude the current tag
        tpc_dict = defaultdict(list)
        tpc_list = TagChildren.objects.filter(parent__in=tag_parent_list).exclude(child=tag).select_related('child')
        for tpc in tpc_list:
            tpc_dict[tpc.parent_id].append(tpc.child)
        for tag_parent in tag_parent_list:
            tag_parent.children_list = sorted(tpc_dict.get(tag_parent.id, []), key=lambda p: p.slug)

        return self.render_to_response({
            'tag': tag,
            'tag_children_list': tag_children_list,
            'tag_parent_list': tag_parent_list,
            'video_list': tag.video_set.order_by('-created_on'),
        })


class TagListView(ProtectedTemplateView):

    template_name = 'tag/tag-list.html'

    def get(self, request):
        tag_list = Tag.objects.order_by('slug')
        return self.render_to_response({
            'tag_list': tag_list,
        })
