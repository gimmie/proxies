import os
import gimmie
import urllib2
import unittest

class TestGimmie(unittest.TestCase):
  # setups
  def new_ApiProxy(self):
    proxy = gimmie.ApiProxy(oauth_key=os.environ['OAUTH_KEY'], oauth_secret=os.environ['OAUTH_SECRET'], url_prefix=os.environ['URL_PREFIX'], cookie_key=os.environ['COOKIE_KEY'])
    return proxy
  def http_200_ok(self, content = None):
    res = lambda:0
    res.info = lambda:res
    res.headers = []
    res.code = 200
    res.msg = "OK"
    res.read = lambda: content
    return res
  def new_Client(self):
    client = self.new_ApiProxy().client
    return client

  # tests
  def test_ApiProxy_call_should_launch_correct_url(self):
    original_urlopen = urllib2.urlopen
    try:
      def should_launch_correct_url(url):
        self.assertTrue(url.startswith(os.environ['URL_PREFIX'] + '/1/redeem.json?'))
        self.assertTrue(url.endswith('&email=1&reward_id=1'))
        return self.http_200_ok()
      urllib2.urlopen = should_launch_correct_url
      start_response = lambda status, headers:0
      environ = { 'wsgi.url_scheme': 'http', 'HTTP_HOST': 'test.host', 'PATH_INFO': '/some/where', 'QUERY_STRING': 'gimmieapi=/1/redeem.json?reward_id=1&email=1' }
      proxy = self.new_ApiProxy()
      proxy.__call__(environ = environ, start_response = start_response)
    finally:
      urllib2.urlopen = original_urlopen

  def test_Client_getJSON_should_return_parsed_json(self):
    original_urlopen = urllib2.urlopen
    try:
      urllib2.urlopen = lambda url: self.http_200_ok('{"hello": "world"}')
      client = self.new_Client()
      json = client.getJSON('/1/redeem.json?reward_id=1&email=1')
      self.assertTrue(hasattr(json, 'has_key'))
      self.assertTrue(json.has_key("hello"))
      self.assertEqual(json["hello"], "world")
    finally:
      urllib2.urlopen = original_urlopen

