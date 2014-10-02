from django.conf.urls import patterns, include, url
from django.contrib import admin
from cal import views

admin.autodiscover()

urlpatterns = patterns('',
                       url(r"^$", views.month, name="month"),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r"^(\d+)/$", views.main, name="main"),
                       url(r"^month/(?P<year>\w+)/(?P<month>\w+)/$", views.month, name="month"),
                       url(r"^month/(?P<year>\d+)/(?P<month>\d+)/(?P<change>prev|next)/$", "cal.views.month"),
                       url(r"^day/(\d+)/(\d+)/(\d+)/$", views.day),
                       url(r'^day2/$', 'cal.views.entry_listview', name='entry-list'),
                       url(r'^day2/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/create/$', 'cal.views.entry_create', name='entry-create'),
                       url(r'^day2/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'cal.views.entry_listview', name='entry-list'),
                       url(r"^day/delete/$", 
                       views.DeleteEntryView.as_view(), name="delete_entry"),
                       url(r"^day/(?P<pk>\d+)/delete/$", 
                       views.DeleteEntryView.as_view(), name="delete_entry"),
                       url(r"^settings/$", "settings"),
                       )
