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
	var proxy = new gimmie.ApiProxy({
		'cookie_key':   process.env['COOKIE_KEY'],
		'oauth_key':    process.env['OAUTH_KEY'],
		'oauth_secret': process.env['OAUTH_SECRET'],
		'url_prefix':  'https://api.gimmieworld.com'
	});

You can now use `proxy.proxy` function as callback for anything that processes the `http.ServerRequest` and `http.ServerResponse` pair.

NOTE: the code above presumes your OAuth credentials and other config is stored as environment variables: `COOKIE_KEY`, `OAUTH_KEY` and `OAUTH_SECRET`

### Express.JS

	var express = require("express");
	var app = express();
	app.get('/gimmie/api', proxy.proxy.bind(proxy));
	app.listen(8080);

Note that the actual path mounted does not matter, `gimmie.ApiProxy` can be mounted on any path

### Connect

	var connect = require('connect');
	connect().use(proxy.proxy.bind(proxy)).listen(8080);

### http.Server

	var http = require('http');
	http.createServer(proxy.proxy.bind(proxy)).listen(8080);

## What's this proxy for?

Talking to [Gimmie APIs](https://portal.gimmieworld.com/documentation/json) from the server-side should not be an issue for most developers since the technology stack consists of standards like `HTTP`, `OAuth` and `JSON`.

However, client apps that run on the browser would have problems securing their `OAuth` credentials. The solution is to run a reverse proxy on your own infrastructure and have the client apps talk (without OAuth) to the OAuth configured reverse proxy (which would relay the request to `api.gimmieworld.com` and echo the response back to the browser)

Meaning, a browser request to

 * `http://www.yourserver.com/some/path?gimmieapi=/1/stores.json?hello=world` would be forwarded to
 * `http://api.gimmieworld.com/1/stores.json?hello=world`

When referencing the [API documentation](https://portal.gimmieworld.com/documentation/json), simply replace the url prefix `http://api.gimmieworld.com` with your own reverse proxy url. Everything will still apply as-is.
