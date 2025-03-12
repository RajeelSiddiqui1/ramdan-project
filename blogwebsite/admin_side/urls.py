# admin_side/urls.py
from django.urls import path
from . import views

app_name = 'admin_side'  # Updated namespace

urlpatterns = [
    # admin 
    path('', views.dashboard, name='dashboard'),
    # path('admin/signup/', views.admin_signup, name='admin_signup'),
    path('admin/login/', views.admin_login, name='admin_login'),
     path('logout/', views.admin_logout, name='admin_logout'),
    # path('staff/login/', views.staff_login, name='staff_login'),

    # staff 
    path('staff/list/', views.staff_list, name='staff_list'),
    path('staff/create/', views.staff_create, name='staff_create'),
    path('<int:staff_id>/staff/edit/', views.staff_edit, name='staff_edit'),
    path('<int:staff_id>/staff/delete/', views.staff_delete, name='staff_delete'),

    # category 
    path('category/list/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('<int:cat_id>/category/edit/', views.category_edit, name='category_edit'),
    path('<int:cat_id>/category/delete/', views.category_delete, name='category_delete'),

    # blog 
    path('blog/list/', views.blog_list, name='blog_list'),
    path('blog/admin/published/', views.admin_blog_published, name='admin_blog_published'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('<int:blog_id>/blog/detail/', views.blog_detail, name='blog_detail'),
    path('<int:blog_id>/blog/edit/', views.blog_edit, name='blog_edit'),
    path('<int:blog_id>/blog/delete/', views.blog_delete, name='blog_delete'),

    # user_list
    path('user_list/',views.user_list,name='user_list'),

    # countries
    path('country/list/', views.country_list, name='country_list'),
    path('country/create/', views.country_create, name='country_create'),
    path('<int:con_id>/country/edit/', views.country_edit, name='country_edit'),
    path('<int:con_id>/country/delete/', views.country_delete, name='country_delete'),

    
    path('creator_list/', views.creator_list, name='creator_list'),
   
]