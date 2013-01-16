#Gimmie Node.JS Module

This module is Gimmie Proxy for Node.js application which provide handler function (function that have request, response
as arguments.) It also embed simple server for use with Gimmie API if you don't want to add code to current application
and want to configure reverse-proxy to point to Gimmie Proxy directly.

##Setup for Express.js Application

- Install Gimmie npm

        npm install gimmie-node

- Configure proxy with your application OAuth key and secret first.

        var Gimmie = require('gimmie-node');
        Gimmie.configure({
          Gimmie.options.COOKIE_KEY: 'your_cookie_variable_that_supply_for_user_identity',
          Gimmie.options.OAUTH_KEY: 'your_application_oauth_key',
          Gimmie.options.OAUTH_SECRET: 'your_application_oauth_secret'
        });

        //You can change /gimmie/api to other pretty path
        app.get('/gimmie/api', Gimmie.proxy);

- Update api point in widget configuration

        var _gimmie = {
          api: 'http://yourdomain.com/gimmie/api?'
        }

##Setup for Reverse-Proxy style

- Create new node.js application with gimmie in package.json dependencies
- Below is sample proxy code

        var gimmie = require('gimmie-node');

        gimmie.configure({
          'COOKIE': 'cookie_key',
          'OAUTH_KEY': 'oauth_key',
          'OAUTH_SEC': 'oauth_secret'});

        var server = gimmie.server;
        server.start();

- Start application with node <your node.js file>. It will listen on port 8080.
- Point your proxy to this port below is sample nginx configuration

        upstream gimmie {
          server 127.0.0.1:8080;
        }

        server {
          ...
          location /api { proxy_pass http://gimmie; }
        }

- Update api point in widget configuration

        var _gimmie = {
          api: 'http://yourdomain.com/api?'
        }
