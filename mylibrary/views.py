from django.shortcuts import render

# Create your views here.
#from django.shortcuts import render

# Create your views here.
from .models import Reader, Book
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class BookIndexView(generic.ListView):
    template_name = 'mylibrary/bookindex.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        """Return the top five chinese books order by alpha."""
        return Book.objects.filter(
            language='CN'
        ).order_by('name')[:5]


class ReaderIndexView(generic.ListView):
    template_name = 'mylibrary/readerindex.html'
    context_object_name = 'reader_list'

    def get_queryset(self):
        """Return the top five readers order by alpha."""
        return Reader.objects.filter(
            register_date__gte='2012-12-31'
        ).order_by('name')[:5]


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'mylibrary/bookdetail.html'


class ReaderDetailView(generic.DetailView):
    model = Reader
    template_name = 'mylibrary/readerdetail.html'

