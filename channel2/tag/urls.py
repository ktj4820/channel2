from django.conf.urls import patterns, url
from channel2.tag.views import *


urlpatterns = patterns('',

    url(r'^$',                                      TagListView.as_view(), name='tag.list'),

    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/$',         TagView.as_view(), name='tag'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/edit/$',    TagEditView.as_view(), name='tag.edit'),

)

