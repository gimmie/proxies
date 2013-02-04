from gimmie import ApiProxy
import sys
from wsgiref.simple_server import make_server
application = ApiProxy(app = None, oauth_key='GIMMIE_OAUTH_KEY', oauth_secret='OAUTH_SEC', url_prefix='https://api.gimmieworld.com', cookie_key='COOKIE')
# or simply "application = ApiProxy()" if the config values are already set in environment variables OAUTH_KEY, OAUTH_SECRET, URL_PREFIX, COOKIE_KEY
port = len(sys.argv) > 1 and int(sys.argv[1]) or 8000
httpd = make_server('', port, application)
print "Proxying Gimmie API on port %d..." % port
httpd.serve_forever()
