from .models import Book, Bookcart
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.models import User
from mysite.settings import BOOKSINPAGE,MAXPAGEINDEX
from django.http import JsonResponse
import math, json
from django.core import serializers

def show_library(request):
	if request.user.is_authenticated==True:
		context={'login_status':True, 'user':request.user}
	else:
		context={'logout_status':True}

	bookitems=Book.objects.all()
	if pagations(bookitems):
		context['bookitems'],context['totalpages'],context['maxindex']=pagations(bookitems)
	
	return render(request, 'mylibrary/library.html',context)


def fiter_booklist(request):
	context={'result':0}
	filter=request.GET['filter']
	print(filter)
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
		bookitem = Book.objects.get(book_id=bookid)
		bookitem.bookcart=Bookcart(bookname=bookitem.bookname)
		new_bookcart =bookitem.bookcart
		new_bookcart.user=request.user
		new_bookcart.save()
	else:
		context['result']=1
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


class BookIndexView(generic.ListView):
    template_name = 'mylibrary/bookindex.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        return Book.objects.filter(
            language='CN'
        ).order_by('name')


def BookDetail(request,bookid):
	context={}
	if bookid:
		try:
			bookitem = Book.objects.filter(book_id=bookid)
		except Exception as e:
			bookitem=None
		bookitem = serializers.serialize("json", bookitem)
		context['bookitem']=bookitem

	return render(request,'mylibrary/bookdetail.html',context)

 