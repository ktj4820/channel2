import datetime
import binascii
import os

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
import pytz

from channel2.core.responses import HttpResponseXAccel
from channel2.core.utils import get_ip_address, email_alert
from channel2.core.views import ProtectedTemplateView, TemplateView
from channel2.settings import VIDEO_LINK_EXPIRE
from channel2.video.models import Video, VideoLink


class VideoView(ProtectedTemplateView):

    @classmethod
    def get_video_link(cls, request, id):
        video = get_object_or_404(Video, id=id)

        try:
            time_limit = datetime.datetime.now(tz=pytz.UTC) - datetime.timedelta(hours=12)
            link = VideoLink.objects.get(
                video=video,
                ip_address=get_ip_address(request),
                created_by=request.user,
                created_on__gte=time_limit,
            )
            return video, link
        except VideoLink.DoesNotExist:
            pass

        video.views += 1
        video.save()

        link = VideoLink.objects.create(
            video=video,
            key=binascii.hexlify(os.urandom(32)),
            ip_address=get_ip_address(request),
            created_by=request.user,
        )
        return video, link

    def get(self, request, id, slug):
        video, link = self.get_video_link(request, id)
        # url = '{}?{}'.format(reverse('video.link', args=[link.key, video.slug]), request.META.get('QUERY_STRING'))
        url = reverse('video.link', args=[link.key, video.slug])
        return redirect(url)


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

        if link.ip_address != get_ip_address(request):
            return self.render_to_response({'message': self.messages['ip_address_mistmatch']})

        if timezone.now() - link.created_on > timezone.timedelta(seconds=VIDEO_LINK_EXPIRE):
            return self.render_to_response({'message': self.messages['link_expired']})

        download = 'download' in request.GET
        return HttpResponseXAccel(
            url=link.video.url,
            name='{}.mp4'.format(link.video.slug),
            content_type='video/mp4',
            attachment=download
        )
