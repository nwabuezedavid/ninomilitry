from django.contrib import admin
from .models import MilitaryProfile, BlogPost, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_date',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_featured')
    list_filter = ('is_featured', 'published_date', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    inlines = [CommentInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'content')
        }),
        ('Publishing', {
            'fields': ('published_date', 'is_featured'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('featured_image',),
            'classes': ('collapse',)
        }),
    )

@admin.register(MilitaryProfile)
class MilitaryProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'rank', 'years_of_service')
    list_filter = ('branch',)
    search_fields = ('user__username', 'user__email', 'rank')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'branch', 'rank', 'years_of_service')
        }),
        ('Additional Information', {
            'fields': ('bio', 'profile_image'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date', 'approved')
    list_filter = ('approved', 'created_date')
    search_fields = ('author__username', 'text', 'post__title')
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(approved=False)
    disapprove_comments.short_description = "Disapprove selected comments"




from django.contrib import admin
from .models import Rank, Country, Award, Personnel, Achievement

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation')

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('name',)

class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 1

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'rank', 'country', 'years_of_service', 'is_active')
    list_filter = ('rank', 'country', 'is_active')
    search_fields = ('first_name', 'last_name')
    filter_horizontal = ('awards',)
    inlines = [AchievementInline]

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'personnel', 'date')
    list_filter = ('date',)    