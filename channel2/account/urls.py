from django.conf.urls import patterns, url

from channel2.account.views import AccountLoginView


urlpatterns = patterns('',

    url(r'^login/$',        AccountLoginView.as_view(), name='account.login'),

)
