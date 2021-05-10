from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('shortner/<str:hash_cd>', views.shortner, name='shortner'),
    path('list/', views.list_url, name='list_url'),
    path('create/', views.create_url, name='create_url'),
    path('edit/<str:pk>', views.edit_url, name='edit_url'),
    path('delete/', views.delete_url, name='delete_url'),


]