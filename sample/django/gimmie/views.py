from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
def index(request):
	response = redirect('/index.html')
	response.set_cookie('_gm_user', 'test')
	return response

def image_from_api(request):
	return redirect('http://api.lvh.me:3000%s'%request.get_full_path())