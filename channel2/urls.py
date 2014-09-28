from django.conf.urls import patterns, include, url
from django.contrib import admin

from channel2.home.views import HomeView
from channel2.settings import DEBUG, MEDIA_ROOT


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',                  HomeView.as_view(), name='home'),

    # apps
    url(r'^account/',           include('channel2.account.urls')),
    url(r'^admin/',             include(admin.site.urls)),
    url(r'^captcha/',           include('captcha.urls')),
    # url(r'^blog/',              include('channel2.blog.urls')),
    # url(r'^search/',            include('channel2.search.urls')),
    # url(r'^tag/',               include('channel2.tag.urls')),
    # url(r'^staff/',             include('channel2.staff.urls')),
    # url(r'^videos/',            include('channel2.video.urls')),

    # flat urls
    # url(r'',                    include('channel2.flat.urls')),

)


if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    )
