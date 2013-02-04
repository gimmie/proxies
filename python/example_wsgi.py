from gimmie import ApiProxy
import sys
from wsgiref.simple_server import make_server
application = ApiProxy(app = None, route = "/gimmie_proxy", oauth_key='GIMMIE_OAUTH_KEY', oauth_secret='OAUTH_SEC', url_prefix='https://api.gimmieworld.com', cookie_key='COOKIE')
# or simply "application = ApiProxy()" if the config values are already set in environment variables GIMMIE_ROUTE, GIMMIE_OAUTH_KEY, GIMMIE_OAUTH_SECRET, GIMMIE_URL_PREFIX, GIMMIE_COOKIE_KEY
port = len(sys.argv) > 1 and int(sys.argv[1]) or 8000
httpd = make_server('', port, application)
print "Proxying Gimmie API on port %d on %s..." % (port, application.route)
httpd.serve_forever()
