from django.conf.urls import url

from channel2.account import views


urlpatterns = [

    url(r'^login/$',        views.AccountLoginView.as_view(), name='account.login'),

]
