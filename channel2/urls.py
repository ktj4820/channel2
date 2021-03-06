from django.conf.urls import include, url
from django.views.static import serve

from channel2.home.views import HomeView
from channel2.settings import DEBUG, MEDIA_ROOT

urlpatterns = [

    url(r'^$',              HomeView.as_view(), name='home'),

    # apps
    url(r'^account/',       include('channel2.account.urls')),
    url(r'^search/',        include('channel2.search.urls')),
    url(r'^staff/',         include('channel2.staff.urls')),
    url(r'^tag/',           include('channel2.tag.urls')),
    url(r'^video/',         include('channel2.video.urls')),

]


if DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    ]
