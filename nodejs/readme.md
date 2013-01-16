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

