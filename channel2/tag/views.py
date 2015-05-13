from collections import defaultdict
import random

from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect

from channel2.core.views import ProtectedTemplateView
from channel2.tag.enums import TagType
from channel2.tag.models import Tag
from channel2.video.models import Video


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

    def get_context_data(self, id):
        tag = get_object_or_404(Tag, id=id)
        video_list = tag.video_set.order_by('episode', 'name')
        video = None
        if video_list:
            video = video_list[0]
        return {
            'children_list': tag.children.order_by('name'),
            'parent_list': tag.parents.order_by('name'),
            'tag': tag,
            'video': video,
            'video_list': video_list,
        }

    def get(self, request, id, slug):
        context = self.get_context_data(id)
        return self.render_to_response(context)


class TagVideoView(TagView):

    template_name = 'tag/tag.html'

    def get(self, request, id, slug, video_id):
        context = self.get_context_data(id)
        video = get_object_or_404(Video, id=video_id)

        if video not in context['video_list']:
            raise Http404

        context['video'] = video
        return self.render_to_response(context)


class TagRandomView(ProtectedTemplateView):

    def get(self, request):
        id_list = Tag.objects.filter(type=TagType.ANIME).values_list('id', flat=True)
        id = random.choice(id_list)
        tag = Tag.objects.get(id=id)
        return redirect('tag', id=tag.id, slug=tag.slug)
