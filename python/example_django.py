from django.conf.urls import patterns
import gimmie
import django
import os

gimmie_proxy = gimmie.DjangoProxy(oauth_key='OAUTH_KEY', oauth_secret='OAUTH_SEC', url_prefix='https://api.gimmieworld.com', cookie_key='COOKIE', django=django)
urlpatterns = patterns('',
    (r'^gimmie$', gimmie_proxy),
)
