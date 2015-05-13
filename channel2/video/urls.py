from django.conf.urls import url

from channel2.video import views


urlpatterns = [

    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/$',         views.VideoView.as_view(), name='video'),
    url(r'^(?P<key>\w{64})/(?P<slug>[\w-]+).mp4$',  views.VideoLinkView.as_view(), name='video.link'),

]
