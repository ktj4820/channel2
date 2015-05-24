import json
import os

from django.contrib import messages
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.http.response import HttpResponse
from django.shortcuts import redirect, get_object_or_404
import requests

from channel2.account.models import User
from channel2.core.utils import paginate
from channel2.core.views import StaffTemplateView
from channel2.settings import VIDEO_DIR
from channel2.staff import forms
from channel2.staff.formsets import StaffTagVideoFormSet, StaffTagPinnedFormSet
from channel2.tag.models import Tag
from channel2.video.models import Video, VideoLink
from channel2.video.utils import get_episode


class StaffUserView(StaffTemplateView):

    template_name = 'staff/staff-user.html'

    @classmethod
    def get_formset_cls(cls):
        return modelformset_factory(
            model=User,
            extra=0,
            can_delete=True,
            fields=('name', 'is_active', 'is_staff',),
        )

    def get(self, request):
        user_qs = User.objects.order_by('email')
        formset = self.get_formset_cls()(queryset=user_qs)
        return self.render_to_response({
            'form': forms.StaffUserAddForm(),
            'formset': formset,
        })

    def post(self, request):
        user_qs = User.objects.order_by('email')
        formset = self.get_formset_cls()(queryset=user_qs, data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('staff.user')

        return self.render_to_response({
            'form': forms.StaffUserAddForm(),
            'formset': formset,
        })


class StaffUserAddView(StaffTemplateView):

    def post(self, request):
        form = forms.StaffUserAddForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'An activation email has been sent to {}'.format(user.email))
        else:
            messages.error(request, 'An error occurred while trying to add user.')
        return redirect('staff.user')


class StaffAnimeAddView(StaffTemplateView):

    template_name = 'staff/staff-anime-add.html'

    def get(self, request):
        title = request.GET.get('title')
        anime_list = []
        if title:
            anime_list = requests.get('https://hummingbird.me/api/v1/search/anime', {'query': title}).json()
            anime_list = sorted(anime_list, key=lambda i: i['title'])

        data = request.GET if 'title' in request.GET else None
        form = forms.StaffAnimeSearchForm(data=data)

        return self.render_to_response({
            'anime_list': anime_list,
            'form': form,
        })

    def post(self, request):
        form = forms.StaffAnimeAddForm(data=request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect('tag', id=tag.id, slug=tag.slug)

        for field in form.errors:
            for error in form.errors[field]:
                messages.error(request, error)
        return redirect('staff.anime.add')


class StaffTagAddView(StaffTemplateView):

    template_name = 'staff/staff-tag.html'

    def get(self, request):
        return self.render_to_response({
            'form': forms.StaffTagForm(),
        })

    def post(self, request):
        form = forms.StaffTagForm(data=request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect('tag', id=tag.id, slug=tag.slug)

        return self.render_to_response({
            'form': form,
        })


class StaffTagEditView(StaffTemplateView):

    template_name = 'staff/staff-tag.html'

    def get(self, request, id):
        tag = get_object_or_404(Tag, id=id)
        return self.render_to_response({
            'form': forms.StaffTagForm(instance=tag),
            'tag': tag,
        })

    def post(self, request, id):
        tag = get_object_or_404(Tag, id=id)
        form = forms.StaffTagForm(instance=tag, data=request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect('tag', id=tag.id, slug=tag.slug)

        return self.render_to_response({
            'form': form,
            'tag': tag,
        })


class StaffTagVideoView(StaffTemplateView):

    template_name = 'staff/staff-tag-video.html'

    @classmethod
    def get_formset_cls(cls):
        return modelformset_factory(
            model=Video,
            extra=0,
            can_delete=True,
            fields=('name', 'episode',)
        )

    def get_context_data(self, id):
        tag = get_object_or_404(Tag, id=id)
        video_list = Video.objects.filter(tag=tag).order_by('created_on')
        return {
            'tag': tag,
            'video_list': video_list,
        }

    def get(self, request, id):
        context = self.get_context_data(id)
        context['formset'] = self.get_formset_cls()(queryset=context['video_list'])
        return self.render_to_response(context)

    def post(self, request, id):
        context = self.get_context_data(id)
        formset = self.get_formset_cls()(queryset=context['video_list'], data=request.POST)

        if formset.is_valid():
            formset.save()
            return redirect('staff.tag.video', id=id)

        context['formset'] = formset
        return self.render_to_response(context)


class StaffTagAddVideoView(StaffTagVideoView):

    template_name = 'staff/staff-tag-video-add.html'

    @classmethod
    def get_formset_cls(cls):
        return formset_factory(
            form=forms.StaffTagVideoForm,
            formset=StaffTagVideoFormSet,
            extra=0,
            can_order=True,
            max_num=1000)

    def get_initial(self, context):
        initial = []
        for filename in os.listdir(VIDEO_DIR):
            if not filename.endswith('mp4'):
                continue

            episode = get_episode(filename)
            name = context['tag'].name
            if episode:
                name += ' - ' + episode

            initial.append({
                'selected': True,
                'filename': filename,
                'name': name,
                'episode': episode,
            })

        initial = sorted(initial, key=lambda i: i['episode'])
        return initial

    def get(self,  request, id):
        context = self.get_context_data(id)
        initial = self.get_initial(context)
        formset = self.get_formset_cls()(initial=initial)
        context['formset'] = formset
        return self.render_to_response(context)

    def post(self, request, id):
        context = self.get_context_data(id)
        formset = self.get_formset_cls()(data=request.POST)
        if formset.is_valid():
            formset.save(tag=context['tag'])
            return redirect('staff.tag.video.add', id=id)

        context['formset'] = formset
        return self.render_to_response(context)


class StaffTagAutocompleteView(StaffTemplateView):

    def get(self, request):
        tag_list = Tag.objects.order_by('name').values_list('name', flat=True)
        content = json.dumps(list(tag_list), ensure_ascii=False)
        return HttpResponse(content=content, content_type='application/json')


class StaffTagDeleteView(StaffTemplateView):

    def post(self, request, id):
        tag = get_object_or_404(Tag, id=id)
        tag.delete()
        return redirect('tag.list')


class StaffTagPinnedView(StaffTemplateView):

    template_name = 'staff/staff-tag-pinned.html'

    @classmethod
    def get_formset(cls):
        return modelformset_factory(
            model=Tag,
            formset=StaffTagPinnedFormSet,
            fields=[],
            can_order=True,
            extra=0,
        )

    def get_tag_list(self):
        return Tag.objects.filter(pinned=True).order_by('order')

    def get(self, request):
        formset = self.get_formset()(queryset=self.get_tag_list())
        return self.render_to_response({
            'formset': formset,
        })

    def post(self, request):
        formset = self.get_formset()(queryset=self.get_tag_list(), data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('staff.tag.pinned')

        return self.render_to_response({
            'formset': formset,
        })


class StaffVideoActivityView(StaffTemplateView):

    page_size = 50
    template_name = 'staff/staff-video-activity.html'

    def get(self, request):
        link_list = VideoLink.objects.select_related('video', 'created_by').order_by('-created_on')
        link_list = paginate(link_list, self.page_size, request.GET.get('p'))
        return self.render_to_response({
            'link_list': link_list,
        })
