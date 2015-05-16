from collections import defaultdict
import random

from django.shortcuts import get_object_or_404, redirect

from channel2.core.views import ProtectedTemplateView
from channel2.tag.enums import TagType
from channel2.tag.models import Tag
from channel2.tag.utils import convert_season
from channel2.video.models import VideoLink


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

        tag_dict['#'] = sorted(tag_dict['#'], key=lambda t: convert_season(t.name))
        return self.render_to_response({
            'tag_dict': tag_dict,
        })


class TagListAnimeView(TagListView):

    template_name = 'tag/tag-list.html'

    def get_tag_list(self):
        return Tag.objects.filter(type=TagType.ANIME)


class TagView(ProtectedTemplateView):

    template_name = 'tag/tag.html'

    def get(self, request, id, slug, video_id=None):
        tag = get_object_or_404(Tag, id=id)
        video_list = tag.video_set.order_by('episode', 'name')
        video_dict = {str(v.id): v for v in video_list}
        user_video_id_list = VideoLink.objects\
            .filter(video__in=video_list, created_by=request.user)\
            .values_list('video_id', flat=True)\
            .distinct()

        if video_id and video_id in video_dict:
            video = video_dict[video_id]
        else:
            video = None

        if video_list:
            for v in video_list:
                v.watched = v.id in user_video_id_list
                if video is None and not v.watched:
                    video = v
            if video is None:
                video = video_list[0]

        return self.render_to_response({
            'children_list': tag.children.order_by('name'),
            'parent_list': tag.parents.order_by('name'),
            'tag': tag,
            'video': video,
            'video_list': video_list,
        })


class TagRandomView(ProtectedTemplateView):

    def get(self, request):
        id_list = Tag.objects.filter(type=TagType.ANIME).values_list('id', flat=True)
        id = random.choice(id_list)
        tag = Tag.objects.get(id=id)
        return redirect('tag', id=tag.id, slug=tag.slug)
