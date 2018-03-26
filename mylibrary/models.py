# -*- coding:utf-8 -*-
from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class Reader(models.Model):
    READER_TYPE = (
        (0, '游客'),
        (1, '年卡'),
        (2, '月卡'),
        (3, '次卡'),
    )
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=24,blank=True)
    book_limit=models.IntegerField(blank=True, default=0)
    birth_year = models.IntegerField(blank=True, default=2000)
    
    address = models.CharField(max_length=50, blank=True)
    reader_type = models.IntegerField(choices=READER_TYPE, default=0)
    deposit_amount = models.FloatField(default=0)  # 押金
    # register_date = models.DateField(default=timezone.now())
    register_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=datetime.date(2000, 1, 1))
    def bool_expiry(self):
        if datetime.date.today() <= self.expiry_date:
            return False
        else:
            return True

    def __str__(self):
        return User.objects.get(pk=self.user_id).username


class Book(models.Model):
    BOOK_LANGUAGE = (
        ('EN', '英文'),
        ('CN', '中文'),
    )
    AGE_RANGE = (
        (1, '0~2岁'),
        (2, '3~5岁'),
        (3, '6~8岁'),
        (4, '9~12岁'),
        (5, '13+岁'),
    )
    SUBJECTS = (
        (1, '自然'),
        (2, '历史'),
        (3, '数学'),
        (4, '地理'),
        (5, '生物'),
        (6, '故事/小说'),
        (7,'其他'),
    )
    book_id=models.CharField(max_length=13, primary_key=True)  #ISBN number
    bookname = models.CharField(max_length=100, blank=True)
    series_name=models.CharField(max_length=50,blank=True)
    author = models.CharField(max_length=40, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    publish_date=models.CharField(max_length=20,blank=True)
    record_date=models.CharField(max_length=20,blank=True)   #录入系统的时间
    tags = models.CharField(max_length=500,blank=True)
    binding=models.CharField(max_length=10,blank=True)
    translator=models.CharField(max_length=20,blank=True)
    language = models.CharField(max_length=2, choices=BOOK_LANGUAGE, default='EN')
    for_age = models.IntegerField(choices=AGE_RANGE, default=1)
    subject = models.IntegerField(choices=SUBJECTS, default=1)
    pages = models.IntegerField(blank=True,default=0)
    book_count = models.IntegerField(blank=True,default=1)  #图书数量
    image_sm=models.CharField(max_length=50,blank=True)
    image_bg=models.CharField(max_length=50,blank=True)
    summary=models.TextField(max_length=1500,blank=True)
    authorintro=models.TextField(max_length=1500,blank=True)
    catalog=models.CharField(max_length=1500,blank=True)
    price=models.CharField(blank=True,max_length=10)

    def __str__(self):
        return self.bookname
    def save(self):
        self.image_sm='images/'+self.book_id+'.jpg'
        self.image_bg='images/'+self.book_id+'bg.jpg'
        super().save()


class Bookcart(models.Model):
    user = models.CharField(max_length=13)
    book_id=models.ForeignKey(Book,on_delete=models.CASCADE)
    bookname= models.CharField(max_length=80, blank=True)
    add_date=models.DateField(auto_now=True)

class Bookstoreup(models.Model):
    """收藏书单"""
    user = models.CharField(max_length=13)
    book_id=models.ForeignKey(Book,on_delete=models.CASCADE)
    bookname= models.CharField(max_length=80, blank=True)
    add_date=models.DateField(auto_now=True)
        
class SMSCode(models.Model):
    mobilenumber=models.CharField(max_length=11,blank=False)
    randomchar=models.CharField(max_length=6,blank=False)


