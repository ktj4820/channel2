from collections import defaultdict

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from channel2.core.views import ProtectedTemplateView, StaffTemplateView
from channel2.tag.forms import TagForm
from channel2.tag.models import Tag, TagChildren
from channel2.video.models import VideoLink


class TagView(ProtectedTemplateView):

    template_name = 'tag/tag.html'

    def get(self, request, id, slug, video_id=None):
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

        video_list = tag.video_set.order_by('created_on')
        video_dict = {str(v.id): v for v in video_list}
        user_video_id_list = VideoLink.objects.filter(video__in=video_list, created_by=request.user).values_list('video_id', flat=True).distinct()

        if video_id and video_id in video_dict:
            active_video = video_dict[video_id]
        else:
            active_video = None

        for video in video_list:
            video.watched = video.id in user_video_id_list
            if not active_video and not video.watched:
                active_video = video

        return self.render_to_response({
            'active_video': active_video,
            'tag': tag,
            'tag_children_list': tag_children_list,
            'tag_parent_list': tag_parent_list,
            'video_list': video_list,
        })


class TagListView(ProtectedTemplateView):

    template_name = 'tag/tag-list.html'

    def get(self, request):
        tag_list = Tag.objects.order_by('slug')
        return self.render_to_response({
            'tag_list': tag_list,
        })


class TagCreateView(StaffTemplateView):

    template_name = 'tag/tag-edit.html'

    def get(self, request):
        return self.render_to_response({
            'form': TagForm(user=request.user),
        })

    def post(self, request):
        form = TagForm(user=request.user, data=request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, 'Tag "{}" has been created'.format(tag.name))
            return redirect('tag.edit', id=tag.id, slug=tag.slug)

        return self.render_to_response({
            'form': form,
        })


class TagEditView(StaffTemplateView):

    template_name = 'tag/tag-edit.html'

    def get(self, request, id, slug):
        tag = get_object_or_404(Tag, id=id)
        return self.render_to_response({
            'form': TagForm(user=request.user, instance=tag),
            'tag': tag,
        })

    def post(self, request, id, slug):
        tag = get_object_or_404(Tag, id=id)
        form = TagForm(user=request.user, instance=tag, data=request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, 'Tag "{}" has been updated'.format(tag.name))
            return redirect('tag.edit', id=tag.id, slug=tag.slug)

        return self.render_to_response({
            'form': form,
            'tag': tag,
        })


class TagVideoView(StaffTemplateView):

    template_name = 'tag/tag-video.html'

    def get(self, request, id, slug):
        return self.render_to_response({})

    def post(self, request, id, slug):
        return self.render_to_response({})
