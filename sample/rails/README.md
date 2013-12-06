# Introduction

This is a sample plain Rails 3 application that

* was deployed to run at [http://gimmiewidget-with-proxy.herokuapp.com/](http://gimmiewidget-with-proxy.herokuapp.com/)
* hosts a Gimmie Widget in `public/index.html` file
* runs a proxy at `/gimmie_proxy?gimmieapi=` path

# Walk through

## 1. Generic Rails app

First, a generic rails app was created

```
rails new gimmiewidget-with-proxy -d postgres
```

NOTE: Since we're deploying to Heroku, the simplest setup is to use postgresql database. For this reason, we're using `-d postgres` option. Gimmie integration does not depend on it

## 2. Integration work

### 2.1 Add widget

[Create a new widget](https://portal.gimmieworld.com/widgets) at the gimmie portal and paste the `Embed` code into `public/index.html`

### 2.2 Add gem

Add this into `Gemfile`

	gem "gimmie"

Update your `Gemfile.lock` file by executing

	bundle install

### 2.3 Configure proxy route

Add this route into `config/routes.rb`

	match "/gimmie_proxy" => Gimmie::Proxy.new

### 2.4 Configure environment variables

These environment variables will need to be configured for the `gimmie` gem to work

	GIMMIE_OAUTH_KEY
	GIMMIE_OAUTH_SECRET
	GIMMIE_COOKIE_KEY
	GIMMIE_URL_PREFIX

In Heroku, this is done with the `heroku config:add` command line

	heroku config:add GIMMIE_COOKIE_KEY=_gm_key
	heroku config:add GIMMIE_URL_PREFIX=https://api.gimmieworld.com
	heroku config:add GIMMIE_OAUTH_KEY=<YOUR GAME CONSUMER KEY GOES HERE>
	heroku config:add GIMMIE_OAUTH_SECRET=<YOUR GAME CONSUMER SECRET GOES HERE>

NOTE: OAUTH key and secret should be obtained from your `Game Info` page in the gimmie portal.

## 3. Deploy

To deploy on Heroku, first add and commit all the changes then simply `git push heroku master`
