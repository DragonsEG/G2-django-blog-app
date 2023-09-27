from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', views.Index.as_view(), name='index'),
    path('login/', views.loginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('create/', views.createView.as_view(), name="Create"),
    path('blog/<int:pk>/', views.DetailPostView.as_view(), name='detail_post'),
    path('profile/<str:user>/' , views.profileView.as_view() , name = 'profile') ,
    path('delAccount/<str:user>' , views.deleteAccount , name = "deleteAccount") , 
    path('changepassword' , views.changePass.as_view(), name = 'changepassword')

]