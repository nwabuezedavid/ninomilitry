from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog_list'),
    path('logout/', views.logoutuser, name='logout'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('post/new/', views.create_post, name='create_post'),
    path('search/', views.search, name='search'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('personnel', views.personnel, name='personnel'),
    path('personnel/<int:pk>/', views.personnel_detail, name='personnel_detail'),
]