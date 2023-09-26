from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.post_list,name='post_list'),
    path('create/', views.post_create,name='create_post'),
    path('draft/', views.post_draft,name='drafted_post'),
    path('<int:id>/', views.post_detail,name='post_detail'),
]