"""
URL configuration for django_rest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('api.urls')),
    path('blog-post/create/', views.create_blog_post_view, name='create_blog_post'),
    path('blog-post/list/', views.list_blog_posts_view, name='list_blog_posts'),
    path('blog-post/edit/<int:post_id>/', views.edit_blog_post_view, name='edit_blog_post'),

]
