from django.conf.urls import patterns, include, url
from django.contrib import admin
from cal import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'calendario_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r"^(\d+)/$", views.main, name="main"),
	url(r"", views.main, name="main"),
	url(r"^month/(\d+)/(\d+)/(prev|next)/$", "month"),
	url(r"^month/(\d+)/(\d+)/$", "month"),
	url(r"^month$", "month"),
	url(r"^day/(\d+)/(\d+)/(\d+)/$", "day"),
	url(r"^settings/$", "settings"),
)
