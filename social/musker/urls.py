from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('profile-list/',views.profile_list,name='profile_list'),
    path('profile/<int:pk>',views.profile,name='profile'),
    path('login/',views.user_login, name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('register/',views.register_user,name="register"),
    path('update_user/',views.update_user,name="update_user"),
    path("unfollow/<int:pk>",views.unfollow,name="unfollow"),
    path("follow/<int:pk>",views.follow,name="follow"),
    path('profile/followers/<int:pk>',views.followers,name='followers'),
    path('profile/following/<int:pk>',views.following,name='following'),
    path("tweet_likes/<int:pk>",views.tweet_likes,name="tweet_likes"),
    path("tweet_show/<int:pk>",views.tweet_show,name="tweet_show"),
    path("delete_tweet/<int:pk>",views.delete_tweet,name="delete_tweet"),
]
