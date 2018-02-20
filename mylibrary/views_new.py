import datetime
from django.shortcuts import render,redirect,HttpResponse
from io import BytesIO

from respository import models
from utils import pagination
from backend.forms import forms
from utils import check_code
# Create your views here.
from views import RegisterForm

def login(request):
    # print(request.POST)
    if request.method == 'GET':
        obj = forms.loginForm()
        # print('GET')
        return render(request,'login.html',{'form':obj})

    elif request.method == 'POST':
        # print(request.POST)
        obj = forms.loginForm(request.POST)
        errors = {}
        if obj.is_valid():
            post_check_code = request.POST.get('check_code')
            session_check_code = request.session['check_code']
            if post_check_code.lower() == session_check_code.lower() :
            # values = obj.clean()
                data = obj.cleaned_data
                # print(data)
                # print(data)
                # print(obj.errors)
            # print('POST')\
                if request.POST.get('auto_login'):
                    request.session.set_expiry(60 * 60 * 24 *30)
                request.session['is_login'] = 'true'
                request.session['user'] = data.get('username')
                print(request.session['username'])
                return redirect('/')
            else:
                # print(obj.errors)
                errors['check_code'] = '请输入正确的验证码！'
                return render(request, 'login.html', {'form': obj,'errors':errors})

        return render(request,'login.html',{'form':obj})


def logout(request):
    try:
        #删除is_login对应的value值
        del request.session['is_login']
        del request.session['user']
    except KeyError:
        pass
    #点击注销之后，直接重定向回登录页面
    return redirect('/login/')


def register(request):
    if request.method == 'GET':
        obj = RegisterForm()
    elif request.method == 'POST':
        obj = forms.Register(request.POST)
        post_check_code = request.POST.get('check_code')
        session_check_code = request.session['check_code']
        print(post_check_code, session_check_code)
        if obj.is_valid():
            if post_check_code == session_check_code:
                data = obj.cleaned_data
                print(data)
                # models.User.objects.create(
                username = data.get('username')
                password = data.get('pwd')
                email = data.get('email')
                nickname = data.get('username')
                # )
                models.User.objects.create(username=username, nickname=nickname, password=password, email=email)
                request.session['is_login'] = 'true'
                request.session['user'] = data.get('username')
                return redirect('/')
        else:
            errors = obj.errors
            print('hello')

    return render(request, 'register.html', {'form': obj})


def article(request, *args, **kwargs):
    print(kwargs)
    return redirect('/')


# 将check_code包放在合适的位置，导入即可，我是放在utils下面
from utils import check_code


def create_code_img(request):
    f = BytesIO() #直接在内存开辟一点空间存放临时生成的图片
    img, code = check_code.create_validate_code()#调用check_code生成照片和验证码
    request.session['check_code'] = code #将验证码存在服务器的session中，用于校验
    img.save(f, 'PNG') #生成的图片放置于开辟的内存中
    return HttpResponse(f.getvalue())  #将内存的数据读取出来，并以HttpResponse返回


#!/usr/bin/env python
# -*- coding: utf8 -*-
#__Author: "Skiler Hao"
#date: 2017/3/30 15:40
from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator
from respository import models


class RegisterForm(forms.Form):
    username = fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={'class': "form-control",'placeholder': '用户名为8-12个字符'}),
        min_length=6,
        max_length=12,
        strip=True,
        error_messages={'required': '标题不能为空',
                        'min_length': '用户名最少为6个字符',
                        'max_length': '用户名最不超过为20个字符'},
    )
    email = fields.EmailField(
        required=True,
        widget=widgets.TextInput(attrs={'class': "form-control",'placeholder': '请输入邮箱'}),
        strip=True,
        error_messages={'required': '邮箱不能为空',
                        'invalid':'请输入正确的邮箱格式'},
    )
    pwd = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': "form-control",'placeholder': '请输入密码，必须包含数字,字母,特殊字符'},render_value=True),
        required=True,
        min_length=6,
        max_length=12,
        strip=True,
        validators=[
            # 下面的正则内容一目了然，我就不注释了
            RegexValidator(r'((?=.*\d))^.{6,12}$', '必须包含数字'),
            RegexValidator(r'((?=.*[a-zA-Z]))^.{6,12}$', '必须包含字母'),
            RegexValidator(r'((?=.*[^a-zA-Z0-9]))^.{6,12}$', '必须包含特殊字符'),
            RegexValidator(r'^.(\S){6,10}$', '密码不能包含空白字符'),
        ], #用于对密码的正则验证
        error_messages={'required': '密码不能为空!',
                        'min_length': '密码最少为6个字符',
                        'max_length': '密码最多不超过为12个字符!',},
    )
    pwd_again = fields.CharField(
        #render_value会对于PasswordInput，错误是否清空密码输入框内容，默认为清除，我改为不清楚
        widget=widgets.PasswordInput(attrs={'class': "form-control",'placeholder': '请再次输入密码!'},render_value=True),
        required=True,
        strip=True,
        error_messages={'required': '请再次输入密码!',}

    )

    def clean_username(self):
        # 对username的扩展验证，查找用户是否已经存在
        username = self.cleaned_data.get('username')
        users = models.User.objects.filter(username=username).count()
        if users:
            raise ValidationError('用户已经存在！')
        return username

    def clean_email(self):
        # 对email的扩展验证，查找用户是否已经存在
        email = self.cleaned_data.get('email')
        email_count = models.User.objects.filter(email=email).count() #从数据库中查找是否用户已经存在
        if email_count:
            raise ValidationError('该邮箱已经注册！')
        return email

    def _clean_new_password2(self): #查看两次密码是否一致
        password1 = self.cleaned_data.get('pwd')
        password2 = self.cleaned_data.get('pwd_again')
        if password1 and password2:
            if password1 != password2:
                # self.error_dict['pwd_again'] = '两次密码不匹配'
                raise ValidationError('两次密码不匹配！')

    def clean(self):
        #是基于form对象的验证，字段全部验证通过会调用clean函数进行验证
        self._clean_new_password2() #简单的调用而已


class loginForm(forms.Form):
    username = fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={'class': "form-control",'placeholder': '请输入用户名'}),
        min_length=6,
        max_length=12,
        strip=True,
        error_messages={'required': '用户名不能为空',}
    )

    pwd = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': "form-control",'placeholder': '请输入密码'}),
        required=True,
        min_length=6,
        max_length=12,
        strip=True,
        error_messages={'required': '密码不能为空!',}
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        pwd = self.cleaned_data.get('pwd')
        user = models.User.objects.filter(username=username).first()
        if username and pwd:
            if not user :

                # self.error_dict['pwd_again'] = '两次密码不匹配'
                raise ValidationError('用户名不存在！')
            elif pwd != user.password:
                raise ValidationError('密码不正确！')

forms.py
