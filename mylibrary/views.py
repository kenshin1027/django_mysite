# Create your views here.
from .models import Reader, Book
from django.shortcuts import get_object_or_404, render, render_to_response
from django.views import generic
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.forms import widgets
from django.forms import fields
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        required=True,
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '用户名为8-12个字符'}),
        min_length=6,
        max_length=12,
        strip=True,
        error_messages={'required': '标题不能为空',
                        'min_length': '用户名最少为6个字符', },
    )
    #password = forms.CharField(label='密__码', widget=forms.PasswordInput())
    password = forms.CharField(
        label='密 码',
        widget=forms.PasswordInput(attrs={'class': "form-control", }, render_value=True),
        required=True,
        min_length=6,
        max_length=14,
        strip=True,
        validators=[
            RegexValidator(r'((?=.*\d))^.{6,12}$', '必须包含数字'),
            RegexValidator(r'((?=.*[a-zA-Z]))^.{6,12}$', '必须包含字母'),
            RegexValidator(r'((?=.*[^a-zA-Z0-9]))^.{6,12}$', '必须包含特殊字符'),
            RegexValidator(r'^.(\S){6,10}$', '密码不能包含空白字符'),
        ],
        error_messages={'required': '密码不能为空!',
                        'min_length': '密码最少为6个字符',
                        'max_length': '密码最多不超过为12个字符!', }
    )
    password_again = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': '请再次输入密码!'}, render_value=True),
        required=True,
        strip=True,
        error_messages={'required': '请再次输入密码!', }

    )


def register(request):
    method = request.method
    if method == 'POST':
        uf = RegisterForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            try:
                choose_user = User.objects.filter(username=username).get().username
                return render(request, 'mylibrary/register.html', {'choose_user': choose_user})
            except:
                new_user = User.objects.create_user(username=username, password=password)
                new_user.save()
                return render(request, 'mylibrary/register.html', {'username': username})
    else:
        uf = RegisterForm()
        #return render_to_response('mylibrary/register.html', {'uf': uf, 'method': method})#, context_instance=RequestContext(req))
        return render(request, 'mylibrary/register.html', {'uf': uf, 'method': method})


def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                context = {'username': username}
                return render(request, 'mylibrary/index.html', context)
            # response = HttpResponseRedirect('mylibrary/index.html')
            # response.set_cookie('cookie_username', username, 3600)
            # return response
            else:
            #return HttpResponse('用户名或密码错误,请重新登录')
                return HttpResponseRedirect('')
    else:
        uf = UserForm()
        return render(request, 'mylibrary/login.html', {'uf': uf})
        # return render_to_response('mylibrary/login.html', {'userform': userform})


def logout(request):
    response = HttpResponse('logout!<br><a href="127.0.0.1:8000/mylibrary/register>register</a>"')
    response.delete_cookie('cookie_username')
    return response


class BookIndexView(generic.ListView):
    template_name = 'mylibrary/bookindex.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        """Return the top five chinese books order by alpha."""
        return Book.objects.filter(
            language='CN'
        ).order_by('name')[:5]


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'mylibrary/bookdetail.html'


class ReaderDetailView(generic.DetailView):
    model = Reader
    template_name = 'mylibrary/readerdetail.html'


# class RegisterForm(forms.Form):
#     username = fields.CharField(
#         required=True,
#         widget=widgets.TextInput(attrs={'class': "form-control",'placeholder': '用户名为8-12个字符'}),
#         min_length=6,
#         max_length=12,
#         strip=True,
#         error_messages={'required': '标题不能为空',
#                         'min_length': '用户名最少为6个字符',
#                         'max_length': '用户名最不超过为20个字符'},
#     )
#
#     email = fields.EmailField(
#         required=True,
#         widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '请输入邮箱'}),
#         # strip=True,
#         error_messages={'required': '邮箱不能为空', 'invalid': '请输入正确的邮箱格式', },
#     )
#
#     pwd = fields.CharField(
#         widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': '必须包含数字,字母,特殊字符'},
#                                      render_value=True),
#         required=True,
#         min_length=6,
#         max_length=12,
#         strip=True,
#         validators=[
#                 RegexValidator(r'((?=.*\d))^.{6,12}$', '必须包含数字'),
#                 RegexValidator(r'((?=.*[a-zA-Z]))^.{6,12}$', '必须包含字母'),
#                 RegexValidator(r'((?=.*[^a-zA-Z0-9]))^.{6,12}$', '必须包含特殊字符'),
#                 RegexValidator(r'^.(\S){6,10}$', '密码不能包含空白字符'),
#           ],
#         error_messages={'required': '密码不能为空!',
#                         'min_length': '密码最少为6个字符',
#                         'max_length': '密码最多不超过为12个字符!', },
#     )
#     pwd_again = fields.CharField(
#     #render_value会对于PasswordInput，错误是否清空密码输入框内容，默认为清除，我改为不清楚
#         widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': '请再次输入密码!'}, render_value=True),
#         required=True,
#         strip=True,
#         error_messages={'required': '请再次输入密码!', }
#     )
#
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         users = User.objects.filter(username=username).count()
#         if users:
#             raise ValidationError('用户已经存在！')
#             return username
#
#     def clean_email(self):
#         # 对email的扩展验证，查找用户是否已经存在
#         email = self.cleaned_data['email']
#         email_count = User.objects.filter(email=email).count()
#         if email_count:
#             raise ValidationError('该邮箱已经注册！')
#             return email
#
#     def clean_new_password2(self):
#         password1 = self.cleaned_data['pwd']
#         password2 = self.cleaned_data['pwd_again']
#         if password1 and password2:
#             if password1 != password2:
#                 # self.error_dict['pwd_again'] = '两次密码不匹配'
#                 raise ValidationError('两次密码不匹配！')
#
#     def clean(self):
#         #是基于form对象的验证，字段全部验证通过会调用clean函数进行验证
#         self.clean_new_password2()
