from collections import defaultdict

from django.shortcuts import get_object_or_404

from channel2.core.views import ProtectedTemplateView
from channel2.tag.enums import TagType
from channel2.tag.models import Tag


class TagListView(ProtectedTemplateView):

    template_name = 'tag/tag-list.html'

    def get_tag_list(self):
        return Tag.objects.all()

    def get(self, request):
        tag_dict = defaultdict(list)
        for tag in self.get_tag_list():
            k = tag.name[0].upper()
            if k.isdigit(): k = '#'
            tag_dict[k].append(tag)

        for k, v in tag_dict.items():
            tag_dict[k] = sorted(v, key=lambda t: t.name)

        return self.render_to_response({
            'tag_dict': tag_dict,
        })


class TagListAnimeView(TagListView):

    template_name = 'tag/tag-list.html'

    def get_tag_list(self):
        return Tag.objects.filter(type=TagType.ANIME)


class TagView(ProtectedTemplateView):

    template_name = 'tag/tag.html'

    def get(self, request, id, slug):
        tag = get_object_or_404(Tag, id=id)
        video_list = tag.video_set.order_by('name')
        return self.render_to_response({
            'children_list': tag.children.order_by('name'),
            'parent_list': tag.parents.order_by('name'),
            'tag': tag,
            'video_list': video_list,
        })
