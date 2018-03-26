from django.urls import path, re_path
from . import views
app_name = 'mylibrary'


urlpatterns = [
				path('filter_booklist/', views.filter_booklist),
				path('search_booklist/',views.search_booklist),
				path('addbookcart/',views.addbookcart),
				path('addstoreup/',views.addstoreuup),
				re_path('bookid/(?P<bookid>[0-9]{13})/',views.BookDetail),
				path('', views.showlibrary),
]
