# -*- coding: utf-8 -*-
# Create your views here.
from .models import Book
from django.shortcuts import render
from django.views import generic
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import widgets
from django.contrib.auth import authenticate
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    username = forms.CharField(
        label='用户名',
        required=True,
        help_text='选择自己常用的用户名',
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '用户名为4-12个字符'}),
        min_length=4,
        max_length=12,
        strip=True,
        error_messages={'required': '标题不能为空',
                        'min_length': '用户名最少为4个字符', },
    )
    password = forms.CharField(
        label='密 码',
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': '包含字母数字'},  render_value=True),
        required=True,
        min_length=6,
        max_length=18,
        help_text='长度6~18位',
        strip=True,
        validators=[
            RegexValidator(r'((?=.*\d))^.{6,18}$', '必须包含数字'),
            RegexValidator(r'((?=.*[a-zA-Z]))^.{6,18}$', '必须包含字母'),
            # RegexValidator(r'((?=.*[^a-zA-Z0-9]))^.{6,18}$', '必须包含特殊字符'),
            RegexValidator(r'^.(\S){5,17}$', '密码不能包含空白字符'),
        ],
        error_messages={'required': '密码不能为空!',
                        'min_length': '密码最少为6个字符',
                        'max_length': '密码最多不超过为18个字符!', }
    )
    password_again = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': '请再次输入密码'}, render_value=True),
        required=True,
        strip=True,
        error_messages={'required': '请再次输入密码!', }

    )
    # email = forms.EmailField(error_messages={'required': u'邮箱不能为空'})
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入邮箱账号", "value": "", "required": "required", }),
        required=True,
        max_length=30,
        error_messages={"required": "用户名不能为空", }
    )
    captcha = CaptchaField()

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")
        username = cleaned_data.get('username')
        users = User.objects.filter(username=username).count()
        if users:
            error_str = username + "用户已经存在"
            self.add_error('username', error_str)

        if password != password_again:
            self.add_error('password_again', u"两次密码必须一致")



class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=widgets.TextInput(attrs={'class': "form-control",'placeholder': '请输入用户名'}),
        min_length=4,
        max_length=12,
        strip=True,
        error_messages={'required': '用户名不能为空',}
    )

    password = forms.CharField(
        widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': '请输入密码'}),
        required=True,
        # min_length=6,
        max_length=18,
        strip=True,
        error_messages={'required': '密码不能为空!', }
    )
    captcha = CaptchaField()
    def clean(self):
        username = self.cleaned_data.get('username')
        user_count = User.objects.filter(username=username).count()
        if username:
            if not user_count:
                error_str = '不存在' + username
                self.add_error('username', error_str)


def register(request):
    rf = RegisterForm()
    if request.method == 'POST':
        user_input = RegisterForm(request.POST)
        if user_input.is_valid():
            username = user_input.cleaned_data['username']
            password = user_input.cleaned_data['password']
            email = user_input.cleaned_data['email']
            new_user = User.objects.create_user(username=username, password=password, email=email, is_active=0)
            new_user.save()
            return render(request, 'mylibrary/register_success.html', {'username': username})
        else:
            return render(request, 'mylibrary/register.html', {'rf': user_input, 'errors': user_input.errors})
    return render(request, 'mylibrary/register.html', {'rf': rf})


def login(request):
    lf = LoginForm()
    if request.method == 'POST':
        user_input = LoginForm(request.POST)
        print(user_input)
        if user_input.is_valid():
            username = user_input.cleaned_data['username']
            password = user_input.cleaned_data['password']
            user = User.objects.get(username=username)
            if user.is_active:
                user = authenticate(username=username, password=password)
                if user is not None:
                    context = {'user': user}
                    return render(request, 'mylibrary/index.html', context)
                else:
                    LoginForm.add_error(user_input, 'password', '密码错误')
                    #return render(request, 'mylibrary/login.html', {'lf': user_input, 'errors': user_input.errors})
            else:
                LoginForm.add_error(user_input, 'username', '账号未激活')
                #return render(request, 'mylibrary/login.html', {'lf': user_input, 'errors': user_input.errors})

        #else:
        return render(request, 'mylibrary/login.html', {'lf': user_input, 'errors': user_input.errors})
    else:
        return render(request, 'mylibrary/login.html', {'lf': lf})


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


class ActiveAccountForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        required=True,
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '用户名为4-12个字符'}),
        min_length=4,
        max_length=12,
        strip=True,
        error_messages={'required': '标题不能为空',
                        'min_length': '用户名最少为4个字符', },
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "请输入邮箱账号", "value": "", "required": "required", }),
        required=True,
        max_length=30,
        error_messages={"required": "用户名不能为空", }
    )
    captcha = CaptchaField()

    def clean(self):
        username = self.cleaned_data.get('username')
        user_count = User.objects.filter(username=username).count()
        if username:
            if not user_count:
                error_str = '不存在' + username
                self.add_error('username', error_str)


def active_account(request):
    af = ActiveAccountForm()
    if request.method=='POST':
        user_input = ActiveAccountForm(request.POST)
        if user_input.is_valid():
            username = user_input.cleaned_data['username']
            email = user_input.cleaned_data['email']
            email_db = User.objects.get(username=username).email
            if email!=email_db:
                ActiveAccountForm.add_error(user_input, 'email', '邮箱账号不匹配')
            else:
                pass
                # to do tomorrow
        return render(request, 'mylibrary/active.html', {'af': user_input, 'errors': user_input.errors})
    return render(request, 'mylibrary/active.html', {'af':af},)
