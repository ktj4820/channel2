from django.conf.urls import patterns, url
from channel2.label.views import LabelView, LabelListView

urlpatterns = patterns('',

    url(r'^$',                                      LabelListView.as_view(), name='label.list'),
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/$',         LabelView.as_view(), name='label'),

)
