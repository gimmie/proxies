import oauth2 as oauth
import json
import urllib2 
import time

# setup
my_player_uid = 'TEST123'
key = 'e75c0adccf82e8e4a78fbbcdcb71'
secret = '80b8c633533c96cc4835365b6e7f'

access_token = my_player_uid
access_token_secret = secret
consumer = oauth.Consumer(key=key, secret=secret)
token = oauth.Token(key=access_token, secret=access_token_secret)

signature_method = oauth.SignatureMethod_HMAC_SHA1()
params = {
    'oauth_version': "1.0",
    'oauth_nonce': oauth.generate_nonce(),
    'oauth_timestamp': int(time.time()),
    'oauth_token': token.key,
    'oauth_consumer_key': consumer.key,
}

# usage
endpoint = "https://api.gimmieworld.com/1/profile.json"
req = oauth.Request.from_consumer_and_token(consumer, token=token, http_method="GET", http_url=endpoint, parameters=params)
req.sign_request(signature_method, consumer, token)

req_json = urllib2.urlopen(str(req.to_url()))
req_content = json.load(req_json)

json_content = json.dumps(req_content)

print req_content["response"]["success"] # should be true
