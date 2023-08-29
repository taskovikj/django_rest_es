from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.models import CustomUser, BlogPost, UserFollowing, Vote
from base.forms import CustomUserInfoForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from base.views import blog_detail_view
from base.views import get_published_blogs

@login_required
def user_profile_edit(request):
    user = request.user
    blog_posts = BlogPost.objects.filter(author=user, draft=False)
    drafts = BlogPost.objects.filter(author=user, draft=True)
    unpublished = get_unpublished_blogs_for_user(user)
    followers = UserFollowing.objects.filter(following=user).count()
    following = UserFollowing.objects.filter(follower=user).count()

    context = {
        'num_articles': blog_posts.count(),
        'followers': followers,
        'following': following,
        'user': user,
        'blog_posts': blog_posts,
        'drafts': drafts,
        'unpublished': unpublished
    }
    return render(request, 'user/user_profile.html', context)


def author_articles(request,user_id):
    user = get_object_or_404(CustomUser,id=user_id)
    blog_posts = get_published_blogs().filter(author=user)
    articles = True
    return render(request, 'user/author_articles.html', {'blog_posts': blog_posts,
                                                    'articles':articles})

def author_unpublished(request):
    blog_posts = get_unpublished_blogs_for_user(request.user)
    unbublished = True
    return render(request, 'user/author_articles.html', {'blog_posts': blog_posts,
                                                    'unbublished':unbublished})

def author_drafts(request):
    blog_posts = BlogPost.objects.filter(author=request.user,draft=True)
    draft = True
    return render(request, 'user/author_articles.html', {'blog_posts': blog_posts,
                                                    'draft':draft})
def user_profile_view(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    blog_posts = BlogPost.objects.filter(author=user)
    is_following = UserFollowing.objects.filter(follower=request.user,
                                                following=user).exists() if request.user.is_authenticated else False

    followers = UserFollowing.objects.filter(following=user).count()
    following = UserFollowing.objects.filter(follower=user).count()
    context = {
        'num_articles':blog_posts.count(),
        'followers':followers,
        'following': following,
        'user': user,
        'blog_posts': blog_posts,
        'is_following': is_following
    }
    return render(request, 'user/user_profile_view.html', context)

@login_required
def profile_settings(request):
    user = request.user

    if request.method == 'POST':
        form = CustomUserInfoForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = CustomUserInfoForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'user/user_settings.html', context)
def user_articles(requests):
    user = request.user
    articles =get_published_blogs().filter(author=user)
    drafts  = BlogPost.objects.filter(author=user,draft=True)
    unpublished = get_unpublished_blogs_for_user(user)

@login_required
def vote_post(request, blog_id, vote_type):
    post = get_object_or_404(BlogPost, id=blog_id)
    user = request.user

    if vote_type == 'upvote':
        vote_value = Vote.UPVOTE
    elif vote_type == 'downvote':
        vote_value = Vote.DOWNVOTE

    try:
        old_vote = Vote.objects.get(user=user, blog_post=post)
        if old_vote.vote != vote_value:
            old_vote.delete()
            vote = Vote.objects.create(user=user, blog_post=post, vote=vote_value)
    except Vote.DoesNotExist:
        vote = Vote.objects.create(user=user, blog_post=post, vote=vote_value)

    return redirect('blog_detail', blog_id=blog_id)


def follow(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'follow' and not UserFollowing.objects.filter(follower=request.user, following=user).exists():
            UserFollowing.objects.create(follower=request.user, following=user)
        elif action == 'unfollow' and UserFollowing.objects.filter(follower=request.user, following=user).exists():
            UserFollowing.objects.filter(follower=request.user, following=user).delete()

    return redirect('user_profile_view', user_id=user_id)


@login_required
def following_posts_view(request):
    user = request.user
    following_relations = UserFollowing.objects.filter(follower=user)
    following_users = following_relations.values_list('following', flat=True)
    following_posts = BlogPost.objects.filter(author__in=following_users).order_by('-pub_date')


    context = {
        'blog_posts': following_posts,
    }

    return render(request, 'base/list_blogs_by_condition.html', context)



def get_unpublished_blogs_for_user(user):
    current_datetime = timezone.now()
    blog_posts = BlogPost.objects.filter(author=user, scheduled_date__gte=
    current_datetime, draft=False
                                         )
    return blog_posts
