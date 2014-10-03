from django.conf.urls import patterns, url
from django.contrib import admin
from cal import views

admin.autodiscover()

urlpatterns = patterns('',
                       url(r"^$", views.month, name="month"),
                       url(r"^(\d+)/$", views.main, name="main"),
                       url(r"^mes/(?P<year>\w+)/(?P<month>\w+)/$", views.month, name='month'),
                       url(r"^mes/(?P<year>\d+)/(?P<month>\d+)/(?P<change>prev|next)/$", 'cal.views.month'),
                       url(r'^dia/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/criar/$', 'cal.views.entry_create', name='entry-create'),
                       url(r'^dia/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/atualizar/(?P<pk>\d+)/$', 'cal.views.entry_update', name='entry-update'),
                       url(r"^dia/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/deletar/(?P<pk>\d+)/$", 'cal.views.entry_delete', name="entry-delete"),
                       url(r"^dia/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/detalhes/(?P<pk>\d+)/$", 'cal.views.entry_detail', name="entry-detail"),
                       )
