from django.urls import path

from . import views
from .feeds import LatestPostsFeed
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list,name='post_list'),
    
    path('tag/<slug:tag_slug>/', views.post_list,name='post_list_by_tag'),

    # SEO-friendly
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail,name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('<int:post_id>/comment/',views.post_comment,name='post_comment'),

    path('feed/', LatestPostsFeed() , name='post_feed'),
    path('search/', views.post_search,name='post_search'),


    path('home/', views.home , name='home'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.loginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/users/logout.html'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),

    

] 