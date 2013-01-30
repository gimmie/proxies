"""

1. Use this as a library
* e.g. "from gimmie import ApiProxy"
* See block of code at the bottom of this file

2. OR run this script as a self-contained HTTP server
* e.g. python gimmie.py 8080
* You'll need to set the environment variables: OAUTH_KEY, OAUTH_SECRET, COOKIE_KEY=_gm_user, URL_PREFIX=https://api.gimmieworld.com

"""
import wsgiref.util
import urllib2
import oauth2
import json
import Cookie

def get_player_uid(environ, cookie_key):
  if environ.has_key('HTTP_COOKIE'):
    thiscookie = Cookie.SimpleCookie()
    thiscookie.load(environ['HTTP_COOKIE'])
    if thiscookie.has_key(cookie_key):
      return thiscookie[cookie_key].value
  return ''

class ApiProxy:
  def __init__(self, oauth_key, oauth_secret, url_prefix, cookie_key):
    self.cookie_key = cookie_key
    self.client = Client(oauth_key, oauth_secret, url_prefix)

  def __call__(self, environ, start_response):
    url_suffix = wsgiref.util.request_uri(environ).split("gimmieapi=").pop()
    player_uid = get_player_uid(environ, self.cookie_key)
    status, headers, body = self.client.get(url_suffix, player_uid)
    start_response(status, headers)
    return body

class DjangoProxy:
  def __init__(self, oauth_key, oauth_secret, url_prefix, cookie_key, django):
    self.cookie_key = cookie_key
    self.client = Client(oauth_key, oauth_secret, url_prefix)
    self.django = django

  def __call__(self, request):
    url_suffix = request.get_full_path().split("gimmieapi=").pop()
    player_uid = request.COOKIES.get(self.cookie_key)
    status, headers, body = self.client.get(url_suffix, player_uid)
    content_type_value = list(value for (key,value) in headers if key == "Content-Type")
    return self.django.http.HttpResponse(body, content_type=content_type_value.pop() or 'application/json; charset=utf-8')

class Client:
  def __init__(self, oauth_key, oauth_secret, url_prefix, player_uid = None):
    self.oauth_key = oauth_key
    self.oauth_secret = oauth_secret
    self.access_token_secret = oauth_secret
    self.url_prefix = url_prefix
    self.player_uid = player_uid

  def get(self, url_suffix, player_uid = None):
    consumer = oauth2.Consumer(key=self.oauth_key, secret=self.oauth_secret)
    token = oauth2.Token(key=(player_uid or self.player_uid or ''), secret=self.access_token_secret)
    req = oauth2.Request.from_consumer_and_token(consumer, token=token, http_method="GET", http_url=(self.url_prefix + url_suffix))
    req.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    try:
      res = urllib2.urlopen(str(req.to_url()))
      tuples = (tuple(pair.split(': ', 1)) for pair in res.info().headers)
      headers = list((key,value.rstrip()) for (key,value) in tuples if not wsgiref.util.is_hop_by_hop(key))
      status = "%d %s" % (res.code, res.msg)
      return [status, headers, res]
    except urllib2.HTTPError, e:
      return ["%d %s" % (e.code, e.msg), [], e.msg]

  def getJSON(self, url_suffix, player_uid = None):
    status, headers, body = self.get(url_suffix, player_uid)
    return json.load(body)

if __name__ == "__main__":
  import os
  import sys
  from wsgiref.simple_server import make_server
  proxy = ApiProxy(oauth_key=os.environ['OAUTH_KEY'], oauth_secret=os.environ['OAUTH_SECRET'], url_prefix=os.environ['URL_PREFIX'], cookie_key=os.environ['COOKIE_KEY'])
  port = len(sys.argv) > 1 and int(sys.argv[1]) or 8000
  httpd = make_server('', port, proxy)
  print "Proxying Gimmie API on port %d..." % port
  httpd.serve_forever()
