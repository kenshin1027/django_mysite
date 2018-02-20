from django.urls import path
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
               path('bookindex/', views.BookIndexView.as_view(), name='bookindex'),
               path('<int:pk>/book/', views.BookDetailView.as_view(), name='bookdetail'),
               path('<int:pk>/reader/', views.ReaderDetailView.as_view(), name='readerdetail'),
               path('login/', views.login),
               path('register/', views.register),
               path('logout/', views.logout),

]
