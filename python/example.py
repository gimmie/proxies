from gimmie import ApiProxy
import sys
from wsgiref.simple_server import make_server
proxy = ApiProxy(oauth_key='OAUTH_KEY', oauth_secret='OAUTH_SEC', cookie_key='COOKIE', url_prefix='https://api.gimmieworld.com')
port = len(sys.argv) > 1 and int(sys.argv[1]) or 8000
httpd = make_server('', port, proxy)
print "Proxying Gimmie API on port %d..." % port
httpd.serve_forever()
