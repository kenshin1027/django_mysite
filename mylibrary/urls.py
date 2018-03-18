from django.urls import path, re_path
from . import views
app_name = 'mylibrary'
# urlpatterns = [path('', views.index, name='index'),
#                # ex: /polls/5/
#                #path('<int:question_id>/', views.detail, name='detail'),
#                path('<int:question_id>/', views.detail, name='detail'),
#                # ex: /polls/5/results/
#                path('<int:question_id>/results/', views.results, name='results'),
#                # ex: /polls/5/vote/
#                path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

urlpatterns = [
				path('filter_booklist/', views.fiter_booklist),
				path('search_booklist/',views.search_booklist),
				path('add_bookcart/',views.add_bookcart),
				path('add_storeup/',views.add_storeuup),
				# path('<int:pk>/book/', views.BookDetailView.as_view(), name='bookdetail'),
				re_path('bookid/(?P<bookid>[0-9]{13})/',views.BookDetail),
				path('', views.show_library),
]
