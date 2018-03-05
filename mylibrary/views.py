# -*- coding: utf-8 -*-
# Create your views here.
from __future__ import unicode_literals
from .models import Book, SMSCode, Reader
from django.shortcuts import render, HttpResponse
from django.views import generic
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
# from captcha.fields import CaptchaField
from .sendsms import send_single_sms
from .settings import SMSCODELENGTH
import random
from django.http import JsonResponse


def register(request):
	if request.method == 'POST':
		username = request.POST.get('mobile')
		print('username:%s' % username)
		password = request.POST.get('password')
		print('password:%s' % password)
		new_user = User.objects.create_user(username=username, password=password)
		new_user.reader= Reader()
		new_reader=new_user.reader
		new_user.save()
		new_reader.save()

		
		return render(request, 'mylibrary/register_success.html', {'username':username })
	return render(request, 'mylibrary/register.html')


def login(request):
	if request.method == 'POST':
		username = request.POST.get('mobile')
		print('username:%s' % username)
		password = request.POST.get('password')
		print('password:%s' % password)
		user = authenticate(username=username, password=password)
		if user is None:
			return render(request,'mylibrary/login.html',{"error":"密码错误"})
		
		return render(request,'home.html')
	else:
		return render(request, 'mylibrary/login.html')


def logout(request):
    #response = HttpResponse('logout!<br/><a href="/mylibrary/register>register</a>"')

    response = render(request, 'mylibrary/index.html')
    response.delete_cookie('cookie_username')
    return response


class BookIndexView(generic.ListView):
    template_name = 'mylibrary/bookindex.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        return Book.objects.filter(
            language='CN'
        ).order_by('name')


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'mylibrary/bookdetail.html'



def SendSMSCode(request):
	mobilenumber = request.GET['mobile']
	random_charlist=''
	for i in range(SMSCODELENGTH):
		char=str(int(random.random()*10))
		random_charlist=random_charlist+char
	smscode=SMSCode.objects.create(mobilenumber=mobilenumber,randomchar=random_charlist)
	print(random_charlist)
	smscode.save()
	#result=send_single_sms(mobilenumber, random_charlist)
	result={
	"result": 0, 
	"errmsg": "OK",
	"ext": "",
	"nationcode":"86",
	"sid": "xxxxxxx",
	"fee": 1
	}
	result['smscode']=random_charlist;
	return JsonResponse(result)


def CheckRepeatMobile(request):
	mobilenumber=request.GET['mobile']
	user_count = User.objects.filter(username=mobilenumber).count()
	if user_count==1:
		result={'result':1}
	else:
		result={'result':0}
	return JsonResponse(result) 

