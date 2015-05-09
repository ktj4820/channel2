from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
import requests

from channel2.core.views import StaffTemplateView
from channel2.staff.forms import StaffUserAddForm, StaffAnimeSearchForm, StaffAnimeAddForm
from channel2.tag.models import Tag


class StaffUserAddView(StaffTemplateView):

    template_name = 'staff/staff-user-add.html'

    def get(self, request):
        return self.render_to_response({
            'form': StaffUserAddForm(),
        })

    def post(self, request):
        form = StaffUserAddForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'An activation email has been sent to {}'.format(user.email))
            return redirect('staff.user.add')

        return self.render_to_response({
            'form': form,
        })


class StaffAnimeAddView(StaffTemplateView):

    template_name = 'staff/staff-anime-add.html'

    def get(self, request):
        title = request.GET.get('title')
        anime_list = []
        if title:
            anime_list = requests.get('https://hummingbird.me/api/v1/search/anime', {'query': title}).json()
            anime_list = sorted(anime_list, key=lambda i: i['title'])

        data = request.GET if 'title' in request.GET else None
        form = StaffAnimeSearchForm(data=data)

        return self.render_to_response({
            'anime_list': anime_list,
            'form': form,
        })

    def post(self, request):
        form = StaffAnimeAddForm(data=request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect('tag', id=tag.id, slug=tag.slug)

        for field in form.errors:
            for error in form.errors[field]:
                messages.error(request, error)
        return redirect('staff.anime.add')


class StaffTagEditView(StaffTemplateView):

    template_name = 'staff/staff-tag-edit.html'

    def get(self, request, id):
        tag = get_object_or_404(Tag, id=id)
        return self.render_to_response({
            'tag': tag,
        })


class StaffTagVideoView(StaffTemplateView):

    template_name = 'staff/staff-tag-video.html'

    def get(self,  request, id):
        tag = get_object_or_404(Tag, id=id)
        return self.render_to_response({
            'tag': tag,
        })
