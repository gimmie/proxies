var fs = require('fs'),
    gimmie = require('gimmie-node'),
    http = require('http'),
    https = require('https'),
    mime = require('mime'),
    path = require('path'),
    querystring = require('querystring'),
    url = require('url');

var Cookies = require('cookies');
var ApiProxy = gimmie.ApiProxy;

var endpoint = 'http://api.gm.llun.in.th:3000';

var api = new ApiProxy({
  'cookie_key':   '_gm_user',
  'oauth_key':    '734b7a763b0346b90533543abe84',
  'oauth_secret': '9855c257de10f5266d218e2f45b9',
  'url_prefix':   endpoint
});

var server = http.createServer(
  function (req, res) {
    var cookies = new Cookies(req, res);
    var target = url.parse(req.url).pathname;

    if (target === '/') {
      target += 'index.html';
    }

    if (target === '/gimmie') {
      api.proxy(req, res);
      return;
    }
    else if (/^\/system/.test(target)) {
      try {
        var service = http;
        if (/^https/.test(endpoint)) {
          service = https;
        }
        service.get(endpoint + req.url, function (proxy) {
          res.writeHead(proxy.statusCode, proxy.headers);
            proxy.pipe(res);
          });
      } catch (e) {
        res.writeHead(404, {});
        res.end();
      }
      return;
    }

    var _path = path.join(__dirname, '..', 'static', target);
    if (fs.existsSync(_path)) {

      var _url = url.parse(req.url);
      var _query = querystring.parse(_url.query);
      if (_query) {
        if (_query['user']) {
          cookies.set('_gm_user', _query['user']);
        }
      }

      res.writeHead(200, {
        'Content-Type': mime.lookup(_path)
      });

      var fileStream = fs.createReadStream(_path);
      fileStream.pipe(res);
    }
    else {
      res.writeHead(404, {
        'Content-Type': 'text/plain'
      });
      res.end('Not Found');
    }
  });

server.listen(8080, '0.0.0.0');
console.log ('server listen on 8080');

process.on('uncaughtException', function (err) {
  console.log (err);
  console.log (err.stack);
  process.exit(-1);
});