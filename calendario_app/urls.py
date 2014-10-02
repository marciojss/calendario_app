from django.conf.urls import patterns, include, url
from django.contrib import admin
from cal import views

admin.autodiscover()

urlpatterns = patterns('',
                       url(r"^$", views.month, name="month"),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r"^(\d+)/$", views.main, name="main"),
                       url(r"^month/(?P<year>\w+)/(?P<month>\w+)/$", views.month, name="month"),
                       url(r"^month/(?P<year>\d+)/(?P<month>\d+)/(?P<change>prev|next)/$", 'cal.views.month'),
                       url(r'^day2/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/create/$', 'cal.views.entry_create', name='entry-create'),
                       url(r'^day2/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<pk>\d+)/update/$', 'cal.views.entry_update', name='entry-update'),
                       url(r"^day2/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<pk>\d+)/delete/$", 'cal.views.entry_delete', name="entry-delete"),
                       url(r"^day2/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<pk>\d+)/detail/$", 'cal.views.entry_detail', name="entry-detail"),
                       url(r"^settings/$", "settings"),
                       )
