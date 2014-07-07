from django.conf.urls import patterns, url
from channel2.account.views import AccountLoginView, AccountLogoutView, \
    AccountActivateView, AccountPasswordResetView, AccountPasswordSetView


urlpatterns = patterns('',

    url(r'^login/$',            AccountLoginView.as_view(), name='account.login'),
    url(r'^logout/$',           AccountLogoutView.as_view(), name='account.logout'),

    url(r'^password/reset/$',                       AccountPasswordResetView.as_view(), name='account.password.reset'),
    url(r'^password/reset/(?P<token>\w{64})/$',     AccountPasswordSetView.as_view(), name='account.password.set'),

    url(r'^activate/(?P<token>\w{64})/$',       AccountActivateView.as_view(), name='account.activate'),

)
