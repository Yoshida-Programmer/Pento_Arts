from django.urls import path
from . import views
from .admin import mypage_site

app_name = 'pento_app'

urlpatterns = [
    path('mypage/', mypage_site.urls, name='mypage'),
    path('', views.index, name='index'),
    path('<slug:username>/edit', views.edit, name='edit'),
    path('create/', views.create, name='create'),
    path('<slug:username>', views.detail, name='detail'),
    path('delete/<int:pk>', views.delete, name='delete'), 
    path('<str:username>/delete/', views.userdelete, name='userdelete'),
    path('like/', views.like, name='like'),
    path('settings/', views.settings, name='settings'),
    path('<slug:username>/follow', views.follow_view, name='follow'),
    path('<slug:username>/unfollow', views.unfollow_view, name='unfollow'),
]
