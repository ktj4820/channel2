from django.conf.urls import patterns, url
from channel2.blog.views import BlogView, BlogPostEditView


urlpatterns = patterns('',

    url(r'^$',                                  BlogView.as_view(), name='blog'),
    url(r'^new/$',                              BlogPostEditView.as_view(), name='blog.post.add'),
    url(r'^(?P<id>\d+)/(?P<slug>\w+)/edit/',    BlogPostEditView.as_view(), name='blog.post.edit'),

)
