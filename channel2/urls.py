from django.conf.urls import patterns, include, url
from django.contrib import admin
from channel2.settings import MEDIA_ROOT, DEBUG
from channel2.video.views import VideoListView


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',                  VideoListView.as_view(), name='video.list'),

    # apps
    url(r'^account/',           include('channel2.account.urls')),
    url(r'^admin/',             include(admin.site.urls)),
    url(r'^labels/',            include('channel2.label.urls')),
    url(r'^videos/',            include('channel2.video.urls')),

)

if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    )
