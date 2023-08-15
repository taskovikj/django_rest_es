from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone
# Create your models here.
from django.db.models.signals import Signal
from django.dispatch import receiver
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    STATUS = (
        ('author','author'),
        ('moderator', 'moderator')
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100,choices=STATUS,default='author')
    bio = models.TextField("bio",max_length=600, default="", blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',default='profile_pictures/profile-icon-9.png')

    def __str__(self):
        return self.username




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


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    draft = models.BooleanField(default=False)


class UserFollowing(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')

    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('follower', 'following')



class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


from django.db import models
from django.contrib.auth import get_user_model

class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = (
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)


comment_posted = Signal()
@receiver(comment_posted, sender=Comment)
def send_comment_notification(sender, instance, **kwargs):
    post = instance.post
    if post.author != instance.user:
        subject = 'New Comment on Your Article'
        message = f"Hello {post.author.username},\n\nA new comment has been posted on your article '{post.title}'.\n\nComment: {instance.content}\n\nVisit your article to see the comment."
        from_email = 'your-email@example.com'
        recipient_list = [post.author.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=True)