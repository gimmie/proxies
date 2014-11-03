# Gimmie Rack Library

This gem is Rack application to provide a reverse proxy for Gimmie REST API

## Installation

	gem install gimmie

If you are using `bundler`, add this into your `Gemfile`

	gem "gimmie"

### Configuration

Gimmie Proxy library prefers configuration to be set as environment variables

	GIMMIE_OAUTH_KEY
	GIMMIE_OAUTH_SECRET
	GIMMIE_COOKIE_KEY
	GIMMIE_URL_PREFIX

In this way, the `Gimmie::Proxy` object can be simply initialized as

	Gimmie::Proxy.new

Alternatively, configuration can be set as constructor arguments, e.g.

	Gimmie::Proxy.new({
		cookie_key: '_gm_key',
		oauth_key: 'onetwothree',
		oauth_secret: 'fourfivesix',
		url_prefix: 'https://api.gimmieworld.com',
	})

### Rack

Create a file `config.ru` with the following code

	require 'gimmie'
	run Gimmie::Proxy.new

Next, execute the command

	rackup

This will run a web server on port 9292. You can test by sending a HTTP request, e.g.

    curl -i 'http://localhost:9292/gimmieapi=/1/rewards.json'

If your `GIMMIE_URL_PREFIX` is `https://api.gimmieworld.com`, then an OAuth request will sent to `https://api.gimmieworld.com/1/rewards.json` and the response will be echoed back

### Rails

To add Gimmie Proxy into your existing Rails application, simply provide a route in your `config/routes.rb` file, e.g.

	get "/gimmie_proxy" => Gimmie::Proxy.new

Restart your rails application.

You can test by sending a HTTP request, e.g.

    curl -i 'http://localhost:3000/gimmie_proxy?gimmieapi=/1/rewards.json?x=y'

NOTE: the mount path can be anything, Gimmie Proxy does not care; it only looks for the `gimmieapi=` string and ignore everything that comes before.

If your `GIMMIE_URL_PREFIX` is `https://api.gimmieworld.com`, then an OAuth request will sent to `https://api.gimmieworld.com/1/rewards.json?x=y` and the response will be echoed back

## What's this proxy for?

Talking to [Gimmie APIs](https://portal.gimmieworld.com/documentation/json) from the server-side should not be an issue for most developers since the technology stack consists of standards like `HTTP`, `OAuth` and `JSON`.

However, client apps that run on the browser would have problems securing their `OAuth` credentials. The solution is to run a reverse proxy on your own infrastructure and have the client apps talk (without OAuth) to the OAuth configured reverse proxy (which would relay the request to `api.gimmieworld.com` and echo the response back to the browser)

Meaning, a browser request to

 * `http://www.yourserver.com/some/path?gimmieapi=/1/stores.json?hello=world` would be forwarded to
 * `http://api.gimmieworld.com/1/stores.json?hello=world`

When referencing the [API documentation](https://portal.gimmieworld.com/documentation/json), simply replace the url prefix `http://api.gimmieworld.com` with your own reverse proxy url. Everything will still apply as-is.
