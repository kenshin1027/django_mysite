"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import show_homepage, login, register, forgetpsw, SendSMSCode, CheckRepeatMobile
from django.contrib.auth.views import logout
urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('mylibrary/', include('mylibrary.urls')),
    # path('captcha/', include('captcha.urls')),
    path('',show_homepage),
    path('logout/', logout),
    path('login/', login),
    path('register/', register),
    path('forgetpsw/', forgetpsw),
    path('sendsms/',SendSMSCode),
    path('checkrepeatmobile/',CheckRepeatMobile),
    ]
