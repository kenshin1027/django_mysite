from .models import Book
from django.views import generic
from django.shortcuts import render

def show_library(request):
	if request.user.is_authenticated==True:
		context={'login_status':True, 'user':request.user}
	else:
		context={'logout_status':True}
	return render(request, 'mylibrary/library.html',context)



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
 