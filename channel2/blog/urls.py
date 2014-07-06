from django.conf.urls import patterns, url
from channel2.blog.views import BlogView


urlpatterns = patterns('',

    url(r'^$',          BlogView.as_view(), name='blog'),

)
