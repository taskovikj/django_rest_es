from django.core.mail import send_mail
from django.db.models.signals import Signal
from django.db.models.signals import post_save
from django.dispatch import receiver

from .indexes import BookIndex
from .models import Book
from .models import Comment

comment_posted = Signal()


@receiver(comment_posted, sender=Comment)
def send_comment_notification(sender, instance, **kwargs):
    post = instance.post
    if post.author != instance.user:
        subject = 'New Comment on Your Article'
        message = f"Hello {post.author.username},\n\nA new comment has been posted on your article '{post.title}'.\n\nComment: {instance.body}\n\nVisit your article to see the comment."
        from_email = 'your-email@example.com'
        recipient_list = [post.author.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=True)


@receiver(post_save, sender=Book)
def index_book(sender, instance, **kwargs):
    book = instance
    BookIndex.init()
    BookIndex(meta={'id': book.id}, title=book.title, description=book.description).save()
