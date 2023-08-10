from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('add/',views.addData),
    path('authors/',views.getAuthors),
    path('add_author/',views.add_author),
    path('books/',views.getBooks),
    path('search/', views.search_items, name='search_items'),

]