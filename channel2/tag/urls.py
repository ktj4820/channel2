from django.conf.urls import patterns, url
from channel2.tag.views import TagView, TagListView, TagEditView, TagVideoView


urlpatterns = patterns('',

    url(r'^$',                                                      TagListView.as_view(), name='tag.list'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/$',                         TagView.as_view(), name='tag'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/(?P<video_id>\d+)/$',       TagView.as_view(), name='tag'),

    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/edit/$',                    TagEditView.as_view(), name='tag.edit'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/videos/$',                  TagVideoView.as_view(), name='tag.video'),

)
