from collections import defaultdict

from channel2.core.views import ProtectedTemplateView
from channel2.tag.enums import TagType
from channel2.tag.models import Tag


class TagListView(ProtectedTemplateView):

    template_name = 'tag/tag-list.html'

    def get(self, request):
        tag_dict = defaultdict(list)
        for tag in Tag.objects.all():
            k = tag.name[0].upper()
            if k.isdigit(): k = '#'
            tag_dict[k].append(tag)

        return self.render_to_response({
            'tag_dict': tag_dict,
        })


class TagListAnimeView(ProtectedTemplateView):

    template_name = 'tag/tag-list-anime.html'

    def get(self, request):
        tag_list = Tag.objects.filter(type=TagType.ANIME).order_by('name')
        return self.render_to_response({
            'tag_list': tag_list,
        })
