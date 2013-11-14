from django.conf.urls import patterns, include, url
from channel2.video.views import VideoListView


urlpatterns = patterns('',

    url(r'^$',                  VideoListView.as_view(), name='video.list'),

    # apps
    url(r'^account/$',          include('channel2.account.urls')),

)
