from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("group/<slug:slug>/", views.group_posts, name="group"),
    path("new/", views.new_post, name="new_post"),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/', views.post_detail, name='post'),
    path('follow/', views.follow_index, name='follow_index'),
    path('profile/<str:username>/unfollow/', views.profile_unfollow, name='profile_unfollow'),
    path('profile/<str:username>/follow/', views.profile_follow, name='profile_follow'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
