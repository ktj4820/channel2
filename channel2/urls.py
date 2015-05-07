from django.conf.urls import include, url

from channel2.home.views import HomeView


urlpatterns = [

    url(r'^$',              HomeView.as_view(), name='home'),

    # apps
    url(r'^account/',       include('channel2.account.urls')),
    url(r'^staff/',         include('channel2.staff.urls')),
    url(r'^tag/',           include('channel2.tag.urls')),

]
