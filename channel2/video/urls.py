from django.conf.urls import patterns, url

from channel2.video.views import VideoView, VideoLinkView, VideoHistoryView, \
    VideoHistoryDeleteView, VideoDeleteView


urlpatterns = patterns('',

    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/$',         VideoView.as_view(), name='video'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/delete/$',  VideoDeleteView.as_view(), name='video.delete'),

    url(r'^(?P<key>\w{64})/(?P<slug>[\w-]+).mp4$',  VideoLinkView.as_view(), name='video.link'),

    url(r'^history/$',          VideoHistoryView.as_view(), name='video.history'),
    url(r'^history/delete/$',   VideoHistoryDeleteView.as_view(), name='video.history.delete'),

)
