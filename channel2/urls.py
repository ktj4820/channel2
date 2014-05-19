from django.conf.urls import patterns, include, url

from channel2.settings import DEBUG, MEDIA_ROOT
from channel2.video.views import VideoListView


urlpatterns = patterns('',

    url(r'^$',                  VideoListView.as_view(), name='video.list'),

    # apps
    url(r'^account/',           include('channel2.account.urls')),
    url(r'^tag/',               include('channel2.tag.urls')),
    # url(r'^search/',            include('channel2.search.urls')),
    url(r'^staff/',             include('channel2.staff.urls')),
    url(r'^videos/',            include('channel2.video.urls')),

    # flat urls
    # url(r'',                    include('channel2.flat.urls')),

)


if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    )
