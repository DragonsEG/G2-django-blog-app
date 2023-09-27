from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', views.Index.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('create/', views.createView.as_view(), name="Create"),
    path('blog/<int:pk>/', views.DetailPostView.as_view(), name='detail_post'),


]