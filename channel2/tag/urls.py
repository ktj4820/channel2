from django.conf.urls import patterns, url
from channel2.tag.views import TagView, TagListView, TagEditView, TagVideoView, \
    TagCreateView, TagDeleteView


urlpatterns = patterns('',

    url(r'^$',                                                      TagListView.as_view(), name='tag.list'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/$',                         TagView.as_view(), name='tag'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/(?P<video_id>\d+)/$',       TagView.as_view(), name='tag'),

    url(r'^new/$',                                                  TagCreateView.as_view(), name='tag.create'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/edit/$',                    TagEditView.as_view(), name='tag.edit'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/delete/$',                  TagDeleteView.as_view(), name='tag.delete'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/videos/$',                  TagVideoView.as_view(), name='tag.video'),

)
