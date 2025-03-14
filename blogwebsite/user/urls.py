from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    # path('logout/', views.logout, name='logout'),
    path('', views.home_page, name="index"),
    path('<int:blog_id>/detail/', views.detail, name="detail"),
    path('blog/<int:blog_id>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('create/', views.blog_create, name="create"),
    path('content_creator_page/', views.content_creator_page, name="content_creator_page"),
    path('content_creator_form/', views.content_creator_form, name="content_creator_form"),
    path('creator_login/', views.creator_login, name="creator_login"),
    path('creator/<int:creator_id>/', views.creator_profile, name='creator_profile'),
    path('follow/<int:creator_id>/', views.toggle_follow, name='toggle_follow'),
    path('creator_list/', views.creator_list, name='creator_list'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('contact_us_list/', views.contact_us_list, name='contact_us_list'),
    path('contact_us_delete/<int:contact_id>', views.contact_us_delete, name='contact_us_delete'),
    path('following/', views.following_list, name='following_list'),
    path('unfollow/<int:creator_id>/', views.unfollow_creator, name='unfollow_creator'),
    path('home/<int:blog_id>/load-more-comments/', views.load_more_comments, name='load_more_comments')
]
