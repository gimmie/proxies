var fs = require('fs'),
    gimmie = require('gimmie-node'),
    http = require('http'),
    mime = require('mime'),
    path = require('path'),
    querystring = require('querystring'),
    url = require('url');

var Cookies = require('cookies');

gimmie.configure({
  'COOKIE'    : '_gm_user',
  'OAUTH_KEY' : 'd883ceb9d02d6b73eae54464075f',
  'OAUTH_SEC' : '0212f8ad3bd4c900fe3784dae456',

  // This is special configuration, using in test machine only
  '_endpoint' : 'http://api.lvh.me:3000'
});

var server = http.createServer(
  function (req, res) {
    var cookies = new Cookies(req, res);
    var target = url.parse(req.url).pathname;

    if (target === '/') {
      target += 'index.html';
    }

    if (target === '/api' && gimmie.proxy) {
      gimmie.proxy(req, res);
      return;
    }
    else if (/^\/system/.test(target)) {
      http.get(gimmie._endpoint + req.url, function (proxy) {
        res.writeHead(proxy.statusCode, proxy.headers);
        proxy.pipe(res);
      });
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