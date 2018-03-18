from .models import Book, Bookcart, Bookstoreup
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.models import User
from mysite.settings import BOOKSINPAGE,MAXPAGEINDEX,MAXBOOKSINBOOKCART
from django.http import JsonResponse
import math, json
from django.core import serializers

def show_library(request):
	context={}
	bookitems=Book.objects.all()
	if bookitems.count():
		context['bookitems'],context['totalpages'],context['maxindex']=pagations(bookitems)
	return render(request, 'mylibrary/library.html',context)


def fiter_booklist(request):
	context={'result':0}
	filter=request.GET['filter']
	language_filter=json.loads(filter)['lang']
	subject_filter=json.loads(filter)['subject']
	age_filter=json.loads(filter)['age']
	pageindex=int(json.loads(filter)['pageindex'])
	if len(language_filter)!=1:
		language_filter=['CN','EN']

	if ((len(subject_filter)==0) or (len(subject_filter)==7)):
		subject_filter=[1,2,3,4,5,6,7]

	if ((len(age_filter)==0) or (len(age_filter)==5)):
		age_filter=[1,2,3,4,5]

	bookitems = Book.objects.filter(language__in= language_filter,subject__in=subject_filter,for_age__in=age_filter)
	if bookitems:
		context['bookitems'],context['totalpages'],context['maxindex']=pagations(bookitems)
	else:
		context['result']=1
	
	if pageindex>1:         #翻页
		if math.ceil(bookitems.count()/BOOKSINPAGE)>pageindex:
			bookitems=bookitems[(pageindex-1)*BOOKSINPAGE:pageindex*BOOKSINPAGE]
		else:
			bookitems=bookitems[(pageindex-1)*BOOKSINPAGE:]
		bookitems = serializers.serialize("json", bookitems)
		context['bookitems']=bookitems
	return JsonResponse(context) 


def search_booklist(request):
	context={'result':0}
	searchtext=request.GET['searchtext']
	bookitems = Book.objects.filter(bookname__icontains=searchtext)
	bookitems_author = Book.objects.filter(author__icontains=searchtext)
	bookitems=bookitems|bookitems_author

	if bookitems:
		context['bookitems'],context['totalpages'],context['maxindex']=pagations(bookitems)
	else:
		context['result']=1
	return JsonResponse(context) 


def add_bookcart(request):
	context={'result':0}
	if request.user.is_authenticated:
		bookid=request.GET['bookid']
		bookcart =Bookcart.objects.filter(user=request.user,book_id=bookid)
		if bookcart.count()==MAXBOOKSINBOOKCART:
			context['result']=2
		if not bookcart:
			bookitem = Book.objects.get(book_id=bookid)
			new_bookcart=Bookcart(bookname=bookitem.bookname,book_id=bookitem)
			new_bookcart.user=request.user
			new_bookcart.save()
		else:
			context={'result':1}
	else:
		context['result']=3
	return JsonResponse(context)


def add_storeuup(request):
	context={'result':0}
	if request.user.is_authenticated:
		bookid=request.GET['bookid']
		bookstoreup =Bookstoreup.objects.filter(user=request.user,book_id=bookid)
		if not bookstoreup:
			bookitem=Book.objects.get(book_id=bookid)
			new_bookstoreup=Bookstoreup(bookname=bookitem.bookname,book_id=bookitem)
			new_bookstoreup.user=request.user
			new_bookstoreup.save()
		else:
			context['result']=1
	else:
		context['result']=2
	return JsonResponse(context)

def pagations(bookitems):
	totalbooks=bookitems.count()
	if totalbooks>0:
		totalpages=math.ceil(totalbooks/BOOKSINPAGE)
		if totalpages>1:
			bookitems=bookitems[0:BOOKSINPAGE]	#一次最多取 BOOKSINPAGE本书的数据
		else:
			bookitems=bookitems[0:]

		if totalpages>MAXPAGEINDEX:		
			maxindex=MAXPAGEINDEX							#max page index in intial booklibrary window
		else:
			maxindex=totalpages
		bookitems = serializers.serialize("json", bookitems)
		return bookitems, totalpages,maxindex
	return False


def BookDetail(request,bookid):
	context={}
	try:
		bookitem = Book.objects.filter(book_id=bookid)
		bookitem = serializers.serialize("json", bookitem)
		context['bookitem']=bookitem
	except Exception as e:
		bookitem=None
		context={'error':'不存在这本书'}
	context['bookid']=bookid
	return render(request,'mylibrary/bookdetail.html',context)

 