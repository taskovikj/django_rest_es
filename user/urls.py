from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile_edit, name='user_profile'),
    path('profile/<int:user_id>/', views.user_profile_view, name='user_profile_view'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('blog-post/vote/<int:blog_id>/<str:vote_type>/', views.vote_post, name='vote_post'),
    path('following/posts/', views.following_posts_view, name='following_posts'),

]
