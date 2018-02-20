# -*- coding:utf-8 -*-
from django.db import models
import datetime
from django.contrib.auth.models import User


class Reader(models.Model):
    READER_TYPE = (
        (0, '游客'),
        (1, '年卡'),
        (2, '月卡'),
        (3, '次卡'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_year = models.IntegerField(blank=True, default=2000)
    phone_number = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=50, blank=True)
    reader_type = models.IntegerField(choices=READER_TYPE, default=0)
    deposit_amount = models.FloatField(default=0)  # 押金
    register_date = models.DateField(default=datetime.date.today())
    #default=datetime.date.today()
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
        ('nature', '自然'),
        ('history', '历史'),
        ('math', '数学'),
        ('geography', '地理'),
        ('biology', '生物'),
    )
    name = models.CharField(max_length=30, blank=True)
    author = models.CharField(max_length=20, blank=True)
    publisher = models.CharField(max_length=20, blank=True)
    language = models.CharField(max_length=2, choices=BOOK_LANGUAGE, default='CN')
    for_age = models.IntegerField(choices=AGE_RANGE, default=1)
    subject = models.CharField(max_length=12, choices=SUBJECTS, default='nature')

    def __str__(self):
        return self.name
# Create your models here.
