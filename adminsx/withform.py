# Add these imports to your admin.py
from .admin_forms import (
    AdminBlogPostForm, AdminCommentForm, AdminMilitaryProfileForm,
    AdminUserCreationForm, AdminUserChangeForm
)
from .admin_actions import (
    export_posts_as_csv, mark_posts_as_featured, remove_posts_from_featured,
    approve_selected_comments, disapprove_selected_comments, export_users_with_profiles
)

# Then update your admin classes to use these forms

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = AdminBlogPostForm
    # ... rest of the class remains the same
    actions = [export_posts_as_csv, mark_posts_as_featured, remove_posts_from_featured]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = AdminCommentForm
    # ... rest of the class remains the same
    actions = [approve_selected_comments, disapprove_selected_comments]

@admin.register(MilitaryProfile)
class MilitaryProfileAdmin(admin.ModelAdmin):
    form = AdminMilitaryProfileForm
    # ... rest of the class remains the same
    actions = [export_users_with_profiles]

# Register a custom User admin to create military profiles automatically
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    
    # ... rest of the class can remain the same as the default UserAdmin

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)