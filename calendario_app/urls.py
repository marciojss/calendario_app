from django.conf.urls import patterns, include, url
from django.contrib import admin
from cal import views

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r"^(\d+)/$", views.main, name="main"),
                       url(r"^month/(?P<year>\w+)/(?P<month>\w+)/$", views.month, name="month"),
                       url(r"^month/$", views.month),
                       url(r"^month/(?P<year>\d+)/(?P<month>\d+)/(?P<change>prev|next)/$", "cal.views.month"),
                       url(r"^day/(\d+)/(\d+)/(\d+)/$", views.day),
                       url(r"^settings/$", "settings"),
                       url(r"", views.main, name="main"),
                       )
