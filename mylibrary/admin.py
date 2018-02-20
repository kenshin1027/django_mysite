# -*- coding:utf-8 -*-
from django.contrib import admin

from .models import Book, Reader
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3
# #admin.site.register(Question)


class ReaderInline(admin.StackedInline):
    model = Reader
    can_delete = False
    verbose_name_plural = 'reader'


class UserAdmin(BaseUserAdmin):
    inlines = [ReaderInline, ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class BookAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ('Question description', {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date']}),
    # ]
    # inlines = [ChoiceInline]
    list_display = ('name', 'author', 'for_age', 'language')
    list_filter = ['name']
    search_fields = ['name']


admin.site.register(Book, BookAdmin)
admin.site.register(Reader)
# Register your models here.
