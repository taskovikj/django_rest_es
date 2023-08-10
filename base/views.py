from django.shortcuts import render, get_object_or_404, redirect
from .forms import BlogPostForm
from .models import BlogPost

def create_blog_post_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user
        BlogPost.objects.create(title=title, content=content,author=author)
        return redirect('list_blog_posts')  # Redirect to list view

    return render(request, 'blog_post_form.html')  # Render the template


def edit_blog_post_view(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        blog_post.title = title
        blog_post.content = content
        blog_post.save()
        return redirect('list_blog_posts')  # Redirect to list view

    return render(request, 'edit_blog_post.html', {'blog_post': blog_post})

def list_blog_posts_view(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'list_blog_posts.html', {'blog_posts': blog_posts})


