import unittest
import urllib2
import gimmie
import os
import random

class TestGimmie(unittest.TestCase):
  # setups
  def http_200_ok(self, content = None):
    res = lambda:0
    res.info = lambda:res
    res.headers = []
    res.code = 200
    res.msg = "OK"
    res.read = lambda: content
    return res
  def new_Client(self):
    client = gimmie.ApiProxy().client
    return client

  # tests
  def test_ApiProxy_call_should_launch_correct_url(self):
    original_urlopen = urllib2.urlopen
    try:
      def should_launch_correct_url(url):
        self.assertTrue(url.startswith(os.environ.get('GIMMIE_URL_PREFIX') + '/1/redeem.json?'))
        self.assertTrue(url.endswith('&email=1&reward_id=1'))
        return self.http_200_ok()
      urllib2.urlopen = should_launch_correct_url
      start_response = lambda status, headers:0
      environ = { 'wsgi.url_scheme': 'http', 'HTTP_HOST': 'test.host', 'PATH_INFO': '/some/where', 'QUERY_STRING': 'gimmieapi=/1/redeem.json?reward_id=1&email=1' }
      proxy = gimmie.ApiProxy()
      proxy.__call__(environ = environ, start_response = start_response)
    finally:
      urllib2.urlopen = original_urlopen

  def test_ApiProxy_should_use_first_argument_as_wsgiapp(self):
    x = random.random()
    proxy = gimmie.ApiProxy(x)
    self.assertEqual(proxy.app, x)

  def test_ApiProxy_use_settings_provided_but_fallback_to_environment_variables(self):
    x = random.random()
    proxy = gimmie.ApiProxy(url_prefix=x)
    self.assertEqual(proxy.client.url_prefix, x)
    self.assertNotEqual(os.environ.get('GIMMIE_OAUTH_SECRET'), None)
    self.assertEqual(proxy.client.oauth_secret, os.environ.get('GIMMIE_OAUTH_SECRET'))

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

  def test_Client_should_use_settings_provided_but_fallback_to_environment_variables(self):
    x = random.random()
    client = gimmie.Client(url_prefix=x)
    self.assertEqual(client.url_prefix, x)
    self.assertNotEqual(os.environ.get('GIMMIE_OAUTH_SECRET'), None)
    self.assertEqual(client.oauth_secret, os.environ.get('GIMMIE_OAUTH_SECRET'))

  def test_DjangoProxy_should_use_settings_provided_but_fallback_to_environment_variables(self):
    x = random.random()
    proxy = gimmie.DjangoProxy(x, url_prefix=x)
    self.assertEqual(proxy.django, x)
    self.assertEqual(proxy.client.url_prefix, x)
    self.assertNotEqual(os.environ.get('GIMMIE_OAUTH_SECRET'), None)
    self.assertEqual(proxy.client.oauth_secret, os.environ.get('GIMMIE_OAUTH_SECRET'))

  def test_ApiProxy_routeMatches_match_everything_by_default(self):
    proxy = gimmie.ApiProxy()
    self.assertTrue(proxy.routeMatches("/def"))
    self.assertTrue(proxy.routeMatches("/"))
    self.assertTrue(proxy.routeMatches(""))
    self.assertTrue(proxy.routeMatches(None))

  def test_ApiProxy_route_returns_true_if_match(self):
    proxy = gimmie.ApiProxy(route="/def")
    self.assertTrue(proxy.routeMatches("/def"))
    self.assertFalse(proxy.routeMatches(None))

  def test_ApiProxy_route_returns_false_if_not_match(self):
    proxy = gimmie.ApiProxy(route="/abc")
    self.assertFalse(proxy.routeMatches("/abcd"))
