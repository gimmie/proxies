import gimmie

from django.http import HttpResponse
from django.shortcuts import redirect

import logging

logger = logging.getLogger(__name__)
client = gimmie.Client(oauth_key='d883ceb9d02d6b73eae54464075f', oauth_secret='0212f8ad3bd4c900fe3784dae456', url_prefix='http://api.lvh.me:3000')

# Create your views here.
def index(request):
	response = redirect('/index.html')
	return response

def image_from_api(request):
	return redirect('http://api.lvh.me:3000%s'%request.get_full_path())

def proxy(request):
	url_suffix = request.get_full_path().split("gimmieapi=").pop()
	player_uid = request.get_signed_cookie('_gm_user', False)
	if not player_uid:
		player_uid = 'test'
	
	url_suffix = request.get_full_path().split("gimmieapi=").pop()
	status, headers, body = client.get(url_suffix, player_uid)
	
	response = HttpResponse(body, content_type='application/json')
	return response