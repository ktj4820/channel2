from django.conf.urls import include, url

urlpatterns = [

    url('^account/',        include('channel2.account.urls')),

]
