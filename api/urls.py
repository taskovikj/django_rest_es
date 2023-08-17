from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.getData),
    path('api/add/',views.addData),
    path('api/authors/',views.getAuthors),
    path('api/add_author/',views.add_author),
    path('api/books/',views.getBooks),
    path('search/', views.search_items, name='search_items'),

]