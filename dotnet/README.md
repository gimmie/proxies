# Gimmie .Net Proxy

Create a Controller for your project. Use the code in ProxyController.cs for your controller file. Update the Gimmie Key, Gimmie Secret and detect your User ID and pass in accordingly. Load /proxy?gimmieapi=/1/login.json.


## What's this proxy for?

Talking to [Gimmie APIs](https://portal.gimmieworld.com/documentation/json) from the server-side should not be an issue for most developers since the technology stack consists of standards like `HTTP`, `OAuth` and `JSON`.

However, client apps that run on the browser would have problems securing their `OAuth` credentials. The solution is to run a reverse proxy on your own infrastructure and have the client apps talk (without OAuth) to the OAuth configured reverse proxy (which would relay the request to `api.gimmieworld.com` and echo the response back to the browser)

Meaning, a browser request to

 * `http://www.yourserver.com/some/path?gimmieapi=/1/stores.json?hello=world` would be forwarded to
 * `http://api.gimmieworld.com/1/stores.json?hello=world`

When referencing the [API documentation](https://portal.gimmieworld.com/documentation/json), simply replace the url prefix `http://api.gimmieworld.com` with your own reverse proxy url. Everything will still apply as-is.
