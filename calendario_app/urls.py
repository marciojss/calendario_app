from django.conf.urls import patterns, include, url
from django.contrib import admin
from cal import views

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r"^(\d+)/$", views.main, name="main"),
                       url(r"", views.main, name="main"),
                       url(r"^month/", views.month , name="month"),
                       url(r"^month/(?P<year>\d+)/(?P<month>\d+)/", views.month , name="month"),
                       url(r"^month/(?P<year>\d+)/(?P<month>\d+)/(prev|next)/", views.month, name="month"),
                       url(r"^day/(\d+)/(\d+)/(\d+)/$", "day"),
                       url(r"^settings/$", "settings"),
                       )
