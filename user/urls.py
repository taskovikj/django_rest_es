from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile_edit, name='user_profile'),
    path('profile/<int:user_id>/', views.user_profile_view, name='user_profile_view'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
]
