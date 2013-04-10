# Sample Node.js project and for internal test with widget.

This folder contains sample node.js project for internal test run or show to client.

To use this project, change follow configuration to your server.

## `app.js` file
 
    var endpoint = 'http://yourserver:port'
    var api = new ApiProxy({
      'cookie_key':   '_gm_user',
      'oauth_key':    'oauth_key',
      'oauth_secret': 'oauth_secret',
      'url_prefix':   endpoint
    });

## Widget files

- All Widget src is in GimmieServer project
  - Widget javascript srcs are under app/assets/javascripts/client
  - Widget filters are in controllers/api_controller.rb (class ApiController, before filter)
  - Dev src is in views/api/widget_dev.html.haml
  - Dev spec can access via `http://api.lvh.me:3000/1/widget_dev.html`
