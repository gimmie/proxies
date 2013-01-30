import os
import os.path

from django.conf.urls import patterns, include, url
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj.views.home', name='home'),
    # url(r'^dj/', include('dj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	url(r'^gimmie', 'gimmie.views.proxy'),
	url(r'^$', 'gimmie.views.index'),
	url(r'^system/', 'gimmie.views.image_from_api'),
	url(r'^(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': os.path.abspath(os.path.join(os.getcwd(), '..', 'static'))
	}),
)
