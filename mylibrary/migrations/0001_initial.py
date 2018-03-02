# Generated by Django 2.0.2 on 2018-02-26 09:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('author', models.CharField(blank=True, max_length=20)),
                ('publisher', models.CharField(blank=True, max_length=20)),
                ('language', models.CharField(choices=[('EN', '英文'), ('CN', '中文')], default='CN', max_length=2)),
                ('for_age', models.IntegerField(choices=[(1, '0~2岁'), (2, '3~5岁'), (3, '6~8岁'), (4, '9~12岁'), (5, '13+岁')], default=1)),
                ('subject', models.CharField(choices=[('nature', '自然'), ('history', '历史'), ('math', '数学'), ('geography', '地理'), ('biology', '生物')], default='nature', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_year', models.IntegerField(blank=True, default=2000)),
                ('phone_number', models.CharField(blank=True, max_length=11)),
                ('address', models.CharField(blank=True, max_length=50)),
                ('reader_type', models.IntegerField(choices=[(0, '游客'), (1, '年卡'), (2, '月卡'), (3, '次卡')], default=0)),
                ('deposit_amount', models.FloatField(default=0)),
                ('register_date', models.DateField(default=datetime.date(2018, 2, 26))),
                ('expiry_date', models.DateField(default=datetime.date(2000, 1, 1))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
