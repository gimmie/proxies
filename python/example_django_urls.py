from django.conf.urls import patterns
import gimmie
import django
import os

gimmie_proxy = gimmie.DjangoProxy(django=django, oauth_key='GIMMIE_OAUTH_KEY', oauth_secret='OAUTH_SEC', url_prefix='https://api.gimmieworld.com', cookie_key='COOKIE')
# or simply "gimmie_proxy = gimmie.DjangoProxy()" if the config values are already set in environment variables OAUTH_KEY, OAUTH_SECRET, URL_PREFIX, COOKIE_KEY
urlpatterns = patterns('',
    (r'^gimmie$', gimmie_proxy),
)
