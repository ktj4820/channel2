from collections import defaultdict
import json
import os

from django.contrib import messages
from django.forms.formsets import formset_factory
from django.http.response import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from channel2.core.views import ProtectedTemplateView, StaffTemplateView
from channel2.settings import VIDEO_DIR
from channel2.tag.forms import TagForm, TagVideoForm, TagVideoFormSet
from channel2.tag.models import Tag, TagChildren
from channel2.video.models import VideoLink, Video
from channel2.video.utils import extract_name


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

        if video_list:
            for video in video_list:
                video.watched = video.id in user_video_id_list
                if active_video is None and not video.watched:
                    active_video = video
            if active_video is None:
                active_video = video_list[0]

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


class TagDeleteView(StaffTemplateView):

    def get(self, request, id, slug):
        return HttpResponseNotAllowed(permitted_methods=['post'])

    def post(self, request, id, slug):
        tag = get_object_or_404(Tag, id=id)
        tag.delete()
        messages.error(request, 'Tag "{}" has been deleted'.format(tag.name))
        return redirect('tag.list')


class TagVideoView(StaffTemplateView):

    select_count_default = 10
    template_name = 'tag/tag-video.html'

    @classmethod
    def get_formset_cls(cls):
        return formset_factory(
            form=TagVideoForm,
            formset=TagVideoFormSet,
            extra=0,
            can_order=True,
            max_num=1000,
        )

    def get_context_data(self, id):
        tag = get_object_or_404(Tag, id=id)
        video_list = Video.objects.filter(tag=tag).order_by('created_on')
        return {
            'tag': tag,
            'video_list': video_list,
        }

    def get(self, request, id, slug):
        context = self.get_context_data(id)

        initial = []
        for filename in os.listdir(VIDEO_DIR):
            if os.path.isdir(os.path.join(VIDEO_DIR, filename)):
                continue
            if not filename.endswith('mp4'):
                continue

            initial.append({
                'select': False,
                'filename': filename,
                'name': extract_name(filename),
            })

        initial = sorted(initial, key=lambda i: i['filename'])
        for i in range(min(len(initial), self.select_count_default)):
            initial[i]['select'] = True

        formset = self.get_formset_cls()(initial=initial)
        context['formset'] = formset
        return self.render_to_response(context)

    def post(self, request, id, slug):
        context = self.get_context_data(id)
        formset = self.get_formset_cls()(data=request.POST)
        if formset.is_valid():
            count = formset.save(tag=context['tag'])
            messages.success(request, '{} videos have been improted successfully.'.format(count))
            return redirect('tag.video', id=id, slug=slug)

        context['formset'] = formset
        return self.render_to_response(context)


class TagAutocompleteJsonView(StaffTemplateView):

    def get(self, request):
        tag_list = Tag.objects.order_by('slug').values_list('name', flat=True)
        content = json.dumps(list(tag_list), ensure_ascii=False)
        return HttpResponse(content=content, content_type='application/json')
