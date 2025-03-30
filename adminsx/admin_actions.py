from django.contrib import admin
from django.http import HttpResponse
import csv
import datetime
from .models import BlogPost, Comment, MilitaryProfile

def export_posts_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=blog_posts_{datetime.datetime.now().strftime("%Y%m%d")}.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Author', 'Published Date', 'Featured', 'Comment Count'])
    
    for post in queryset:
        writer.writerow([
            post.title,
            post.author.username,
            post.published_date,
            'Yes' if post.is_featured else 'No',
            post.comments.count()
        ])
    
    return response
export_posts_as_csv.short_description = "Export selected posts to CSV"

def mark_posts_as_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)
mark_posts_as_featured.short_description = "Mark selected posts as featured"

def remove_posts_from_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)
remove_posts_from_featured.short_description = "Remove selected posts from featured"

def approve_selected_comments(modeladmin, request, queryset):
    queryset.update(approved=True)
approve_selected_comments.short_description = "Approve selected comments"

def disapprove_selected_comments(modeladmin, request, queryset):
    queryset.update(approved=False)
disapprove_selected_comments.short_description = "Disapprove selected comments"

def export_users_with_profiles(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=military_users_{datetime.datetime.now().strftime("%Y%m%d")}.csv'
    
    writer = csv.writer(response)
    writer.writerow([
        'Username', 'Email', 'First Name', 'Last Name', 'Date Joined',
        'Branch', 'Rank', 'Years of Service', 'Post Count', 'Comment Count'
    ])
    
    for profile in queryset:
        writer.writerow([
            profile.user.username,
            profile.user.email,
            profile.user.first_name,
            profile.user.last_name,
            profile.user.date_joined,
            profile.get_branch_display(),
            profile.rank,
            profile.years_of_service,
            profile.user.blog_posts.count(),
            profile.user.comments.count()
        ])
    
    return response
export_users_with_profiles.short_description = "Export selected users with profiles to CSV"