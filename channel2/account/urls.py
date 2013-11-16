from django.conf.urls import patterns, url
from channel2.account.views import AccountLogoutView, AccountLoginView, \
    AccountActivateView, AccountCreateView

urlpatterns = patterns('',

    url(r'^login/$',        AccountLoginView.as_view(), name='account.login'),
    url(r'^logout/$',       AccountLogoutView.as_view(), name='account.logout'),
    url(r'^create/',        AccountCreateView.as_view(), name='account.create'),

    url(r'^activate/(?P<token>\w{64})/$',       AccountActivateView.as_view(), name='account.activate'),

)
