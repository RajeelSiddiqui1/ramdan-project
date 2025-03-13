from django.urls import path
from . import views

app_name = 'creator_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.creator_login, name='creator_login'),
    path('logout/', views.creator_logout, name='creator_logout'),
    path('followers/', views.follower_list, name='follower_list'),  # Shortened for clarity
    path('blogs/', views.creator_blog_list, name='blog_list2'),  # Renamed to match conventions
    path('blogs/create/', views.creator_blog_create, name='blog_create'),
    path('blogs/<int:blog_id>/edit/', views.creator_blog_edit, name='blog_edit'),
    path('blogs/<int:blog_id>/delete/', views.creator_blog_delete, name='blog_delete'),
    path('blogs/<int:blog_id>/detail/', views.creator_blog_detail, name='blog_detail'),
    path('blogs/<int:blog_id>/views/', views.blog_views_check, name='blog_views_check'),
    path('stories/', views.creator_story_list, name='stories'),
    path('stories/create/', views.create_story, name='create_story'),
    path('creator/profile/edit/<int:creator_id>', views.creator_profile_edit, name='creator_profile_edit'),
]
