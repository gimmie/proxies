var assert = require('assert');

var OAuth = require('oauth').OAuth;
var Cookies = require('cookies');

var Gimmie = {
  _endpoint: 'https://api.gimmieworld.com',
  _configuration: null,

  options: {
    COOKIE_KEY: 'COOKIE',
    OAUTH_KEY: 'OAUTH_KEY',
    OAUTH_SECRET: 'OAUTH_SEC'
  },

  endpoint_suffix: function(request) {
    return request.url.split('gimmieapi=').pop();
  },

  configure: function (options) {
    assert(options[Gimmie.options.OAUTH_KEY], 'OAUTH_KEY is required');
    assert(options[Gimmie.options.OAUTH_SECRET], 'OAUTH_SECRET is required');

    Gimmie._configuration = {
      cookie_key: options[Gimmie.options.COOKIE_KEY] || '_gm_user',
      oauth_key: options[Gimmie.options.OAUTH_KEY],
      oauth_secret: options[Gimmie.options.OAUTH_SECRET]
    }

    if (options._endpoint) Gimmie._endpoint = options._endpoint;

    Gimmie.OAuth = new OAuth('dont need this', 'dont need this too',
                             Gimmie._configuration.oauth_key,
                             Gimmie._configuration.oauth_secret,
                             '1.0', 'dont need this', 'HMAC-SHA1');

    Gimmie.proxy = function (request, response) {
      var user = '';
      var cookies = new Cookies(request, response);
      if (cookies.get(Gimmie._configuration.cookie_key)) {
        user = cookies.get(Gimmie._configuration.cookie_key);
      }

      var endpoint = Gimmie._endpoint + Gimmie.endpoint_suffix(request);
      Gimmie.OAuth.get(endpoint, user, Gimmie._configuration.oauth_secret,
        function (error, data) {
          response.writeHead(200, {
            'Content-Type': 'application/json'
          });
          response.end(data);
        });

    }
  }

}

module.exports = Gimmie;
