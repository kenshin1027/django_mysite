# -*- coding: utf-8 -*-
# Create your views here.
from __future__ import unicode_literals
from mylibrary.models import SMSCode, Reader
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login as dj_login
from .sendsms import send_single_sms
from .settings import SMSCODELENGTH
import random,json
from django.http import JsonResponse


def register(request):
	if request.method == 'POST':
		username = request.POST.get('mobile')
		password = request.POST.get('password')
		new_user = User.objects.create_user(username=username, password=password)
		new_user.reader = Reader()
		new_reader = new_user.reader
		new_user.save()
		new_reader.save()
		return render(request, 'register_success.html', {'username': username})
	return render(request, 'register.html')


def login(request):
	if request.method == 'POST':
		username = request.POST.get('mobile')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is None:
			return render(request, 'login.html', {"mobile": username, "error": "密码错误"})
		# request.session['user_id'] = user.id
		dj_login(request, user)
		# return render(request,'homepage.html',{'username':username})
		return show_homepage(request)
	else:
		return render(request, 'login.html')

def loginmodal(request):
	context={'result':0}
	username = json.loads(request.POST.get('mobile'))
	password = json.loads(request.POST.get('password'))

	print("username:%s" % username)
	print("password:%s" % password)
	user = authenticate(username=username, password=password)
	if user is None:
		context['result']=1
	else:
		dj_login(request, user)
		context['username']=username
	return JsonResponse(context)



def show_homepage(request):
	if request.user.is_authenticated == True:
		context = {'login_status': True, 'user': request.user}
	else:
		context = {'logout_status': True}
	return render(request, 'homepage.html', context)


def forgetpsw(request):
	if request.method == 'POST':
		username = request.POST.get('mobile')
		user = User.objects.get(username=username)
		user.set_password(username[-6:])
		user.save()
		return render(request, 'reset_psw_success.html')
	return render(request, 'forgetpsw.html')


def SendSMSCode(request):
	mobilenumber = request.GET['mobile']
	random_charlist = ''
	for i in range(SMSCODELENGTH):
		char = str(int(random.random() * 10))
		random_charlist = random_charlist + char
	smscode = SMSCode.objects.create(mobilenumber=mobilenumber, randomchar=random_charlist)
	print(random_charlist)
	smscode.save()
	# result=send_single_sms(mobilenumber, random_charlist)
	result = {
		"result": 0,
		"errmsg": "OK",
		"ext": "",
		"nationcode": "86",
		"sid": "xxxxxxx",
		"fee": 1
	}
	result['smscode'] = random_charlist;
	return JsonResponse(result)


def CheckRepeatMobile(request):
	username = request.GET['mobile']
	user_count = User.objects.filter(username=username).count()
	if user_count == 1:
		result = {'result': 1}
	else:
		result = {'result': 0}
	return JsonResponse(result)
