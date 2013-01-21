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
import Cookie

def player_uid(environ, cookie_key):
  if environ.has_key('HTTP_COOKIE'):
    thiscookie = Cookie.SimpleCookie()
    thiscookie.load(environ['HTTP_COOKIE'])
    if thiscookie.has_key(cookie_key):
      return thiscookie[cookie_key].value
  return ''

class ApiProxy:
  def __init__(self, oauth_key, oauth_secret, cookie_key, url_prefix):
    self.oauth_key = oauth_key
    self.oauth_secret = oauth_secret
    self.access_token_secret = oauth_secret
    self.cookie_key = cookie_key
    self.url_prefix = url_prefix

  def __call__(self, environ, start_response):
    url_suffix = wsgiref.util.request_uri(environ).split("gimmieapi=").pop()
    consumer = oauth2.Consumer(key=self.oauth_key, secret=self.oauth_secret)
    token = oauth2.Token(key=player_uid(environ, self.cookie_key), secret=self.access_token_secret)
    req = oauth2.Request.from_consumer_and_token(consumer, token=token, http_method="GET", http_url=(self.url_prefix + url_suffix))
    req.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    try:
      res = urllib2.urlopen(str(req.to_url()))
      tuples = (tuple(pair.split(': ', 1)) for pair in res.info().headers)
      headers = list((key,value.rstrip()) for (key,value) in tuples if not wsgiref.util.is_hop_by_hop(key))
      status = "%d %s" % (res.code, res.msg)
      start_response(status, headers)
      return res
    except urllib2.HTTPError, e:
      start_response("%d %s" % (e.code, e.msg), [])
      return [e.msg]

if __name__ == "__main__":
  import os
  import sys
  from wsgiref.simple_server import make_server
  proxy = ApiProxy(oauth_key=os.environ['OAUTH_KEY'], oauth_secret=os.environ['OAUTH_SECRET'], cookie_key=os.environ['COOKIE_KEY'], url_prefix=os.environ['URL_PREFIX'])
  port = len(sys.argv) > 1 and int(sys.argv[1]) or 8000
  httpd = make_server('', port, proxy)
  print "Proxying Gimmie API on port %d..." % port
  httpd.serve_forever()
