from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from models import *
import bcrypt


def index(request):
	if 'logged_in' not in request.session:
		return render(request, 'index.html')
	else:
		return redirect('/search')

def login(request):
	msgs = User.objects.loginValidator(request.POST)
	if len(msgs):
		for k,v in msgs.iteritems():
			print k,v
		 	messages.error(request, v, extra_tags=k)
	else:
		user = User.objects.get(user_name=request.POST['user_name'])
		request.session['logged_in'] = user.id
		return redirect('/success')
	
	return redirect('/')

def success(request):
	return redirect('/search')