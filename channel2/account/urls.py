from django.conf.urls import url

from channel2.account import views


urlpatterns = [

    url(r'^login/$',        views.AccountLoginView.as_view(), name='account.login'),
    url(r'^logout/$',       views.AccountLogoutView.as_view(), name='account.logout'),

    url(r'^password/reset/$',                       views.AccountPasswordResetView.as_view(), name='account.password.reset'),
    url(r'^password/reset/(?P<token>\w{64})/$',     views.AccountPasswordSetView.as_view(), name='account.password.set'),
    url(r'^activate/(?P<token>\w{64})/$',           views.AccountActivateView.as_view(), name='account.activate'),

    url(r'^settings/$',     views.AccountSettingsView.as_view(), name='account.settings'),

]
