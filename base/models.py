from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.


from django.contrib.auth.models import AbstractUser




class Items(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    bio = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)
    genre = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)