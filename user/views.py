from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import CustomUser, BlogPost,UserFollowing
from base.forms import CustomUserInforForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

@login_required
def user_profile_edit(request):
    user = request.user
    blog_posts = BlogPost.objects.filter(author=user)

    if request.method == 'POST':
        form = CustomUserInforForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = CustomUserInforForm(instance=user)

    context = {
        'user': user,
        'form': form,
        'blog_posts': blog_posts
    }
    return render(request, 'user/user_profile.html', context)


def user_profile_view(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    blog_posts = BlogPost.objects.filter(author=user)

    context = {
        'user': user,
        'blog_posts': blog_posts
    }
    return render(request, 'user/user_profile_view.html', context)


def follow(request,user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'follow' and not UserFollowing.objects.filter(follower=request.user, following=user).exists():
            UserFollowing.objects.create(follower=request.user, following=user)
        elif action == 'unfollow' and UserFollowing.objects.filter(follower=request.user, following=user).exists():
            UserFollowing.objects.filter(follower=request.user, following=user).delete()


    return redirect('user_profile_view', user_id=user_id)



