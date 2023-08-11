from django.contrib import admin

from .models import Author, Book, BlogPost,CustomUser

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BlogPost)
admin.site.register(CustomUser)