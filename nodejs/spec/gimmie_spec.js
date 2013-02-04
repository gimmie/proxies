var gimmie = require('../gimmie.js');
var proxy = new gimmie.ApiProxy({
  'cookie_key': process.env['GIMMIE_COOKIE_KEY'],
  'oauth_key': process.env['GIMMIE_OAUTH_KEY'],
  'oauth_secret': process.env['GIMMIE_OAUTH_SECRET'],
  'url_prefix': process.env['GIMMIE_URL_PREFIX']
});
var client = proxy.client;

describe("endpoint_suffix", function() {
  it("should take REQUEST_URI, split by 'gimmieapi=' and use the last segment as suffix", function() {
    var request = { url: 'http://lousy.gov/router.jsp?gimmieapi=gimmie.jsphelloworldgimmieapi=/1/rewards.json?reward_id=2&x%20y?1://' };
    expect(proxy.endpoint_suffix(request)).toBe('/1/rewards.json?reward_id=2&x%20y?1://'); // raw value, no parsing whatsoever
  });
});

describe("proxy", function() {
  var result = [];
  var request = {
    pipe: function() { },
    url: 'http://lousy.gov/router.jsp?gimmie.jsp&gimmieapi=/1/rewards.json?reward_id=3', // test data
    headers: {
      'cookie': 'hello=world; ' + proxy.config.cookie_key + '=TEST123; other=cookie'
    }
  }
  var response = {
    writeHead: function() { }
  };
  it("should call correct endpoint url", function() {
    spyOn(client.OAuth, 'get').andCallFake(function(url, player_uid, stuff) {
      expect(url).toBe(proxy.config.url_prefix + '/1/rewards.json?reward_id=3');
      return { on: function() { } };
    });
    proxy.proxy(request, response);
    expect(client.OAuth.get).toHaveBeenCalled();
  })
  it("should pass correct player_uid", function() {
    spyOn(client.OAuth, 'get').andCallFake(function(url, player_uid, stuff) {
      expect(player_uid).toBe('TEST123');
      return { on: function() { } };
    });
    proxy.proxy(request, response);
    expect(client.OAuth.get).toHaveBeenCalled();
  })
  describe("pipe", function() {
    var noop = function() { };
    var oauth_request = { on: noop };
    var oauth_response = {
      statusCode: parseInt(Math.random() * 999),
      headers: { "hello": "world" },
      pipe: noop
    }
    client.OAuth.get = function() { return oauth_request; };
    it("should pipe request", function() {
      spyOn(request, 'pipe').andCallFake(function(target) {
        expect(target).toBe(oauth_request);
      });
      spyOn(oauth_request, 'on', function(event_name, callback) {
        expect(event_name).toBe('response');
      });
      proxy.proxy(request, response);
      expect(request.pipe).toHaveBeenCalled();
      expect(oauth_request.on).toHaveBeenCalled();
    });
    it("should pipe response", function() {
      spyOn(response, 'writeHead').andCallFake(function(status, headers) {
        expect(status).toBe(oauth_response.statusCode);
        expect(headers).toBe(oauth_response.headers);
      })
      spyOn(oauth_response, 'pipe').andCallFake(function(target) {
        expect(target).toBe(response);
      });
      oauth_request.on = function(event_name, callback) { if (event_name == 'response') callback(oauth_response); }
      proxy.proxy(request, response);
      expect(response.writeHead).toHaveBeenCalled();
      expect(oauth_response.pipe).toHaveBeenCalled();
    });
  });
})
