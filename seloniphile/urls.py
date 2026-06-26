"""
URL configuration for instagrame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from seloniphile import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('explore/', views.explore, name='explore'),
    path('', views.login, name='login'),
    path('messages/', views.messages, name='messages'),
    path('messages/<int:pk>', views.messages, name='messages'),
    path('notifications/', views.notifications, name='notifications'),
    path('profile/', views.profile, name='profile'),
    path('reels/', views.reels, name='reels'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('settings/', views.settings, name='settings'),
    path('followers/', views.followers, name='followers'),
    path('following/', views.following, name='following'),
    path('follow_unfollow/<int:pk>', views.follow_unfollow, name='follow_unfollow'),
    path('followers/', views.followers, name='followers'),
    path('remove_followers/<int:pk>', views.remove_followers, name='remove_followers'),
    path('logout/', views.logout, name='logout'),
    path('LikeUnlike/<int:pk>', views.Like_Unlike, name='LikeUnlike'),
    path('comment_post/<int:pk>', views.comment_post, name='comment_post'),
    path('reel_create/', views.reel_create, name='reel_create'),
    path('create_story/', views.create_story, name='create_story'),
    path('view_story/<int:user_id>', views.view_story, name='view_story'),
    path('user_profile/<int:id>/', views.user_profile, name='user_profile')
    


]
