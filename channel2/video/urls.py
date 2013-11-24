from django.conf.urls import patterns, url
from channel2.video.views import VideoView, VideoLinkView, VideoAddView

urlpatterns = patterns('',

    url(r'^add/$',                                  VideoAddView.as_view(), name='video.add'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/$',         VideoView.as_view(), name='video'),
    url(r'^(?P<key>\w{64})/(?P<slug>[\w-]+).mp4$',  VideoLinkView.as_view(), name='video.link'),

)
