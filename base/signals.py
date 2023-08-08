from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book
from .indexes import BookIndex

@receiver(post_save, sender=Book)
def index_book(sender, instance, **kwargs):
    book = instance
    BookIndex.init()
    BookIndex(meta={'id': book.id}, title=book.title, description=book.description).save()
