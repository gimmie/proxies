var gimmie = require('../gimmie.js');
var proxy = new gimmie.ApiProxy({
  'cookie_key': process.env['COOKIE_KEY'],
  'oauth_key': process.env['OAUTH_KEY'],
  'oauth_secret': process.env['OAUTH_SECRET'],
  'url_prefix': process.env['URL_PREFIX']
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
    url: 'http://lousy.gov/router.jsp?gimmie.jsp&gimmieapi=/1/rewards.json?reward_id=3', // test data
    headers: {
      'cookie': 'hello=world; ' + proxy.config.cookie_key + '=TEST123; other=cookie'
    }
  }
  var response = {};
  it("should call correct endpoint url", function() {
    spyOn(client.OAuth, 'get').andCallFake(function(url, player_uid, stuff) {
      expect(url).toBe(proxy.config.url_prefix + '/1/rewards.json?reward_id=3');
    });
    proxy.proxy(request, response);
    expect(client.OAuth.get).toHaveBeenCalled();
  })
  it("should pass correct player_uid", function() {
    spyOn(client.OAuth, 'get').andCallFake(function(url, player_uid, stuff) {
      expect(player_uid).toBe('TEST123');
    });
    proxy.proxy(request, response);
    expect(client.OAuth.get).toHaveBeenCalled();
  })
})
