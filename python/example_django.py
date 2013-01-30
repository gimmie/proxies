from django.conf.urls import patterns, include, url
from gimmie import DjangoProxy
import os
import django

urlpatterns = patterns('',
    (r'^gimmie$', DjangoProxy(oauth_key='OAUTH_KEY', oauth_secret='OAUTH_SEC', url_prefix='https://api.gimmieworld.com', cookie_key='COOKIE', django=django)),
)
