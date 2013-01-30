import os
import os.path

from django.conf.urls import patterns, include, url
from django.http import HttpResponse

import gimmie
import django

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

gimmie_proxy = gimmie.DjangoProxy(oauth_key='d883ceb9d02d6b73eae54464075f', oauth_secret='0212f8ad3bd4c900fe3784dae456', url_prefix='http://api.lvh.me:3000', cookie_key='_gm_user', django=django)
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dj.views.home', name='home'),
    # url(r'^dj/', include('dj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	url(r'^gimmie$', gimmie_proxy),
	url(r'^$', 'gimmie.views.index'),
	url(r'^system/', 'gimmie.views.image_from_api'),
	url(r'^(?P<path>.*)$', 'django.views.static.serve', {
		'document_root': os.path.abspath(os.path.join(os.getcwd(), '..', 'static'))
	}),
)
