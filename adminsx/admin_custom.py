from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from .models import BlogPost, Comment, MilitaryProfile
from .admin_index import military_blog_admin_site
from .admin_forms import (
    AdminBlogPostForm, AdminCommentForm, AdminMilitaryProfileForm,
    AdminUserCreationForm, AdminUserChangeForm
)

# Register models with the custom admin site
class BlogPostAdmin(admin.ModelAdmin):
    form = AdminBlogPostForm
    # ... rest of the class remains the same as in admin.py

class CommentAdmin(admin.ModelAdmin):
    form = AdminCommentForm
    # ... rest of the class remains the same as in admin.py

class MilitaryProfileAdmin(admin.ModelAdmin):
    form = AdminMilitaryProfileForm
    # ... rest of the class remains the same as in admin.py

class CustomUserAdmin(BaseUserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    # ... rest of the class remains the same as in admin.py

# Register with the custom admin site
military_blog_admin_site.register(BlogPost, BlogPostAdmin)
military_blog_admin_site.register(Comment, CommentAdmin)
military_blog_admin_site.register(MilitaryProfile, MilitaryProfileAdmin)
military_blog_admin_site.register(User, CustomUserAdmin)
military_blog_admin_site.register(Group, GroupAdmin)