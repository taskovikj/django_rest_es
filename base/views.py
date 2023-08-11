from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomUserCreationForm
from .models import BlogPost
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
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

def create_blog_post_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user
        BlogPost.objects.create(title=title, content=content,author=author)
        return redirect('index')  # Redirect to list view

    return render(request, 'blog_post_form.html')  # Render the template


def edit_blog_post_view(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        blog_post.title = title
        blog_post.content = content
        blog_post.save()
        return redirect('')  # Redirect to list view

    return render(request, 'edit_blog_post.html', {'blog_post': blog_post})

def index(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'list_blog_posts.html', {'blog_posts': blog_posts})

def blog_detail_view(request, blog_id):
    blog_post = get_object_or_404(BlogPost, id=blog_id)
    return render(request, 'blog_detail.html', {'blog_post': blog_post})


