import oauth2 as oauth
import json
import urllib2 
import time
import urlparse

# configuration 
key = "OAUTH_KEY";
secret = "OAUTH_SEC";
player_uid = 'PLAYER ID'; 

# do not edit after this line
def application(environ, start_response):
  status = '200 OK'
      
  api = environ['REQUEST_URI'];
  
  output = str(gimmie_connect(player_uid,api))
  
  response_headers = [('Content-type', 'application/json'),
  ('Content-Length', str(len(output)))]
  
  start_response(status, response_headers)
  return [output]
  
  
def gimmie_connect(player_uid='', api='', params={}):
    if not player_uid:
        raise ValueError('player_uid cannot be empty')
        
    if not api:
        raise ValueError('api cannot be empty')
    
    access_token = player_uid
    access_token_secret = secret
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    consumer = oauth.Consumer(key=key, secret=secret)
    token = oauth.Token(key=access_token, secret=access_token_secret)
    json_content = ''
    
    api = api.split("gimmieapi=").pop()

    endpoint = "https://api.gimmieworld.com%s" % (api,)

    if endpoint:
        acc_req = oauth.Request.from_consumer_and_token(consumer, token=token, http_method="GET", http_url=endpoint, parameters=params)
                
        acc_req.sign_request(signature_method, consumer, token)
        req_json = urllib2.urlopen(str(acc_req.to_url()))
        req_content = json.load(req_json)
        
        json_content = json.dumps(req_content)

    
    return json_content
  