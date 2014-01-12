import os, binascii
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import ugettext as _
from channel2.core.response import HttpResponseXAccel
from channel2.core.utils import paginate, get_request_ip, email_alert
from channel2.core.views import ProtectedTemplateView, TemplateView, StaffOnlyView
from channel2.label.models import Label
from channel2.settings import VIDEO_LINK_EXPIRE
from channel2.video.forms import VideoAddForm
from channel2.video.models import Video, VideoLink


class VideoListView(ProtectedTemplateView):

    template_name = 'video/video-list.html'
    page_size = 12

    def get(self, request):
        video_list = Video.objects.order_by('-created_on')
        video_list = paginate(video_list, self.page_size, request.GET.get('p'))
        return self.render_to_response({
            'video_list': video_list,
        })


class VideoView(ProtectedTemplateView):

    def get(self, request, id, slug):
        video = get_object_or_404(Video, id=id)
        video.views += 1
        video.save()

        link = VideoLink.objects.create(
            video=video,
            key=binascii.hexlify(os.urandom(32)),
            ip_address=get_request_ip(request),
            created_by=request.user,
        )

        return redirect('video.link', key=link.key, slug=video.slug)


class VideoLinkView(TemplateView):

    template_name = 'video/video-unavailable.html'

    messages = {
        'file_missing': 'Oops! This video no longer exists. An email has been sent to Derek so that he can investigate this.',
        'link_expired': 'The video link has expired. Please reload the video.',
        'ip_address_mistmatch': 'Your ip address has changed. Please reload the video.' ,
    }

    def get(self, request, key, slug):
        link = get_object_or_404(
            VideoLink.objects.select_related('video'),
            key=key,
        )

        if not link.video.file:
            email_alert('[Channel 2] Video File Missing', 'video/video-file-missing-alert.txt', {'video': link.video})
            return self.render_to_response({'message': self.messages['file_missing']})

        if link.ip_address != get_request_ip(request):
            return self.render_to_response({'message': self.messages['ip_address_mistmatch']})

        if timezone.now() - link.created_on > timezone.timedelta(seconds=VIDEO_LINK_EXPIRE):
            return self.render_to_response({'message': self.messages['link_expired']})

        return HttpResponseXAccel(link.video.file, content_type='video/mp4')


class VideoAddView(StaffOnlyView):

    template_name = 'video/video-add.html'

    def get(self, request):
        video = Video.objects.latest('created_on')
        return self.render_to_response({
            'label_list': Label.objects.order_by('slug'),
            'form': VideoAddForm(initial={
                'name': video.name,
                'label': video.label.name,
            }),
        })

    def post(self, request):
        form = VideoAddForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            video = form.save()
            messages.success(request, _('{} has been added.').format(video.name))
            return redirect('video.add')

        return self.render_to_response({
            'label_list': Label.objects.order_by('slug'),
            'form': form,
        })
