import os
import gimmie
import urllib2
import unittest

class TestSequenceFunctions(unittest.TestCase):
  # setups
  def new_ApiProxy(self):
    proxy = gimmie.ApiProxy(oauth_key=os.environ['OAUTH_KEY'], oauth_secret=os.environ['OAUTH_SECRET'], cookie_key=os.environ['COOKIE_KEY'], url_prefix=os.environ['URL_PREFIX'])
    return proxy
  def http_200_ok(self):
    res = lambda:0
    res.info = lambda:res
    res.headers = []
    res.code = 200
    res.msg = "OK"
    return res

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
