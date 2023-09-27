from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F, Sum, Case, When, IntegerField
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CustomUserCreationForm, CommentForm, BlogPostForm, EditBlogPostForm
from .models import BlogPost, Vote
from .models import Comment, Category
from .signals import comment_posted

# from .ml_engine import get_recommendations


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.status = 'author'
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def create_blog_post_view(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)  # Use the form to process the data
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('index')  # Redirect to list view

    else:
        form = BlogPostForm()  # Create a new form instance

    return render(request, 'blog_post_form.html', {'form': form})


@login_required
def edit_blog_post_view(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)

    if request.user != blog_post.author:
        return redirect('index')

    if request.method == 'POST':
        form = EditBlogPostForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to list view

    else:
        form = EditBlogPostForm(instance=blog_post)  # Populate the form with existing data

    return render(request, 'edit_blog_post.html', {'form': form})


from django.utils import timezone


def index(request):
    user_id = request.COOKIES.get('user_id')
    # if user_id is not None:
    #     recommended_posts_id = list(get_recommendations(user_id))
    #     recommended_posts = BlogPost.objects.filter(id__in=recommended_posts_id)

    blog_posts = get_published_blogs()
    annotated_blog_posts = blog_posts.annotate(
        upvote_count=Sum(
            Case(When(vote__vote=Vote.UPVOTE, then=1), default=0, output_field=IntegerField())
        ),
        downvote_count=Sum(
            Case(When(vote__vote=Vote.DOWNVOTE, then=1), default=0, output_field=IntegerField())
        ),
        vote_difference=F('upvote_count') - F('downvote_count')
    )

    blog_posts = get_published_blogs().order_by('-pub_date')

    posts_per_page = 10

    paginator = Paginator(blog_posts, posts_per_page)
    page_number = request.GET.get('page')

    try:
        blog_posts_page = paginator.page(page_number)
    except PageNotAnInteger:
        blog_posts_page = paginator.page(1)
    except EmptyPage:
        blog_posts_page = paginator.page(paginator.num_pages)

    sorted_blog_posts = annotated_blog_posts.order_by('-vote_difference')

    return render(request, 'list_blog_posts.html', {'blog_posts': blog_posts_page,
                                                    'most_liked': sorted_blog_posts, 'user_id1': user_id,
                                                    'recommended_posts': ''})


def blog_detail_view(request, blog_id):
    post = get_object_or_404(BlogPost, id=blog_id)
    comments = Comment.objects.filter(post=post)
    category = post.category
    total_upvotes = post.vote_set.filter(vote=1).count()
    total_downvotes = post.vote_set.filter(vote=-1).count()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            # Emit the comment_posted signal
            comment_posted.send(sender=comment.__class__, instance=comment)

            form = CommentForm()  # Clear the form after saving the comment

    else:
        form = CommentForm()

    context = {
        'blog_post': post,
        'comments': comments,
        'category': category,
        'form': form,
        'total_upvotes': total_upvotes,
        'total_downvotes': total_downvotes,
    }
    return render(request, 'blog_detail.html', context)


@login_required
def category_posts_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    blog_posts = BlogPost.objects.filter(category=category)
    context = {
        'category': category,
        'blog_posts': blog_posts,
    }
    return render(request, 'category_posts.html', context)


def get_published_blogs():
    current_datetime = timezone.now()
    blog_posts = BlogPost.objects.filter(
        Q(scheduled_date__lte=current_datetime) | Q(scheduled_date__isnull=True), draft=False
    )
    return blog_posts


