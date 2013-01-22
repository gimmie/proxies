# Gimmie Node.JS Module

This module is Gimmie Proxy for Node.js application which provide HTTP request handler function. It also embed simple server for use with Gimmie API if you don't want to add code to current application and want to configure reverse-proxy to point to Gimmie Proxy directly.

## Installation

	npm install gimmie-node

## Standalone, streaming, reverse-proxy to Gimmie API server

`gimmie-node` comes with a standalone server that proxies all incoming request to the Gimmie API server. To run it, simply execute

	npm start gimmie-node

This starts a node `http.Server` listening to port 8000 by default. You can customize the port using `npm config`

	npm config set gimmie-node:port 3000
	npm start gimmie-node

The proxy server should listen on port `3000` henceforth.

## Web Frameworks

However, most likely you are already using some web frameworks and you'd like gimmie to proxy within your infrastructure.

In this case, you'd use `gimmie-node` like a library and instantiate a ``gimmie.ApiProxy`` object

	var gimmie = require('gimmie-node');
	var proxy = new ApiProxy({
		'cookie_key':   process.env['COOKIE_KEY'],
		'oauth_key':    process.env['OAUTH_KEY'],
		'oauth_secret': process.env['OAUTH_SECRET'],
		'url_prefix':  'https://api.gimmieworld.com'
	});

You can now use `proxy.proxy` function as callback for anything that processes the `http.ServerRequest` and `http.ServerResponse` pair.

NOTE: the code above presumes your OAuth credentials and other config is stored as environment variables: COOKIE_KEY, OAUTH_KEY and OAUTH_SECRET

### Express.JS

	var app = express.createServer();
	app.get('/gimmie/api', proxy.proxy.bind(proxy));
	app.listen(8080);

Note that the actual path mounted does not matter, `gimmie.ApiProxy` can be mounted on any path

### Connect

	connect().use(proxy.proxy.bind(proxy)).listen(8080);

### http.Server

	require('http').createServer(proxy.proxy.bind(proxy)).listen(8080);
