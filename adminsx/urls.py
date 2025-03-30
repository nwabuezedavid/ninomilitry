from django.urls import path
from . import views

# Admin-specific URL patterns
urlpatterns = [
    # Admin Dashboard
    path('', views.admin_dashboard, name='admin_dashboard'),
    
    # Admin Blog Post Management
    path('posts/', views.admin_post_list, name='admin_post_list'),
    path('posts/create/', views.admin_post_create, name='admin_post_create'),
    path('posts/<int:pk>/', views.admin_post_detail, name='admin_post_detail'),
    path('posts/<int:pk>/edit/', views.admin_post_edit, name='admin_post_edit'),
    path('posts/<int:pk>/delete/', views.admin_post_delete, name='admin_post_delete'),
    path('posts/<int:pk>/feature/', views.admin_post_feature, name='admin_post_feature'),
    path('posts/<int:pk>/publish/', views.admin_post_publish, name='admin_post_publish'),
    path('posts/export/', views.admin_post_export, name='admin_post_export'),
    
    # Admin Comment Management
    path('comments/', views.admin_comment_list, name='admin_comment_list'),
    path('comments/<int:pk>/', views.admin_comment_detail, name='admin_comment_detail'),
    path('comments/<int:pk>/edit/', views.admin_comment_edit, name='admin_comment_edit'),
    path('comments/<int:pk>/delete/', views.admin_comment_delete, name='admin_comment_delete'),
    path('comments/<int:pk>/approve/', views.admin_comment_approve, name='admin_comment_approve'),
    path('comments/export/', views.admin_comment_export, name='admin_comment_export'),
    path('comments/bulk-approve/', views.admin_bulk_approve_comments, name='admin_bulk_approve_comments'),
    path('comments/bulk-disapprove/', views.admin_bulk_disapprove_comments, name='admin_bulk_disapprove_comments'),
    
    # Admin User Management
    path('users/', views.admin_user_list, name='admin_user_list'),
    path('users/<int:pk>/', views.admin_user_detail, name='admin_user_detail'),
    path('users/<int:pk>/toggle-staff/', views.admin_user_toggle_staff, name='admin_user_toggle_staff'),
    path('users/<int:pk>/toggle-active/', views.admin_user_toggle_active, name='admin_user_toggle_active'),
    path('users/export/', views.admin_user_export, name='admin_user_export'),
    
    # Admin Profile Management
    path('profiles/', views.admin_profile_list, name='admin_profile_list'),
    path('profiles/<int:pk>/', views.admin_profile_detail, name='admin_profile_detail'),
    path('profiles/<int:pk>/edit/', views.admin_profile_edit, name='admin_profile_edit'),
    path('profiles/export/', views.admin_profile_export, name='admin_profile_export'),
# urls.py
path('user_profile/<str:username>/', views.user_profile, name='user_profile'),

    
    # Admin Statistics and Reports
    path('statistics/', views.admin_statistics, name='admin_statistics'),
    path('activity-log/', views.admin_activity_log, name='admin_activity_log'),
    
    # Admin AJAX endpoints
    path('ajax/post-stats/', views.admin_ajax_post_stats, name='admin_ajax_post_stats'),
    path('ajax/comment-stats/', views.admin_ajax_comment_stats, name='admin_ajax_comment_stats'),
    path('ajax/user-stats/', views.admin_ajax_user_stats, name='admin_ajax_user_stats'),



    path('peranl/', views.phome, name='phome'),
    path('personnel/<int:pk>/', views.personnel_detail, name='personnel_detail'),
    path('personnel/create/', views.personnel_create, name='personnel_create'),
    path('personnel/<int:pk>/update/', views.personnel_update, name='personnel_update'),
    path('personnel/<int:pk>/delete/', views.personnel_delete, name='personnel_delete'),
]