#!/usr/bin/env node
/*
 * 1. Use this as a library
 * - e.g. var gimmie = require('gimmie');
 * - see block of code at the bottom of this file
 *
 * 2. OR run this script as a self-contained HTTP server
 * - e.g. node gimmie.js 8080
 * - You'll need to set the environment variables: OAUTH_KEY, OAUTH_SECRET, COOKIE_KEY=_gm_user, URL_PREFIX=https://api.gimmieworld.com
 */
var assert = require('assert');
var OAuth = require('oauth').OAuth;
var Cookies = require('cookies');

var Client = function(config) {
  this.config = config;
  this.oauth_secret = config.oauth_secret;
  this.OAuth = new OAuth('unused','unused',config.oauth_key,config.oauth_secret,'1.0','unused','HMAC-SHA1');
}
Client.prototype.get = function(url_suffix, player_uid, callback) {
  var client = this;
  return client.OAuth.get(client.config.url_prefix + url_suffix, player_uid, client.oauth_secret, callback);
}

var ApiProxy = function(config) {
  this.cookie_key = config.cookie_key;
  this.client = new Client(config);
  this.config = config;
}
ApiProxy.prototype.endpoint_suffix = function(request) {
  return request.url.split('gimmieapi=').pop();
}
ApiProxy.prototype.proxy = function(request, response) {
  var proxy = this;
  var cookies = new Cookies(request, response);
  var player_uid = proxy.cookie_key ? cookies.get(proxy.cookie_key) : null;
  var url_suffix = proxy.endpoint_suffix(request);
  var proxy_request = proxy.client.get(url_suffix, player_uid);
  proxy_request.on('error', function(err) {
    response.writeHead(500, {});
    response.end(err.toString())
  });
  proxy_request.on('response', function(proxy_response) {
    proxy_response.pipe(response);
    response.writeHead(proxy_response.statusCode, proxy_response.headers);
  });
  request.pipe(proxy_request)
}

module.exports = {
  ApiProxy: ApiProxy,
  Client: Client
};

if (process.argv[1] == __filename) {
  (function() {
    var proxy = new ApiProxy({
      'cookie_key':   process.env['GIMMIE_COOKIE_KEY'],
      'oauth_key':    process.env['GIMMIE_OAUTH_KEY'],
      'oauth_secret': process.env['GIMMIE_OAUTH_SECRET'],
      'url_prefix':   process.env['GIMMIE_URL_PREFIX']
    });
    var port = process.env.npm_package_config_port || process.argv[2] || 8000;
    require('http').createServer(proxy.proxy.bind(proxy)).listen(port);
    console.log("Proxying Gimmie API on port", port);
  })();
}
