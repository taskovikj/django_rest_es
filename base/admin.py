from django.contrib import admin

from .models import Author, Book, BlogPost,CustomUser, Category

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BlogPost)
admin.site.register(CustomUser)
admin.site.register(Category)