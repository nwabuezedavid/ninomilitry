from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
import csv
import json
from datetime import datetime, timedelta

from app.models import BlogPost, Comment, MilitaryProfile
from app.forms import BlogPostForm, CommentForm, MilitaryProfileForm

# Helper functions
def is_staff(user):
    return user.is_staff

def is_superuser(user):
    return user.is_superuser

# Admin Dashboard
@staff_member_required
def admin_dashboard(request):
    # Get counts
    total_users = User.objects.count()
    total_posts = BlogPost.objects.count()
    total_comments = Comment.objects.count()
    
    # Get recent activity
    recent_posts = BlogPost.objects.order_by('-created_date')[:5]
    recent_comments = Comment.objects.order_by('-created_date')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    # Get statistics
    posts_by_month = BlogPost.objects.filter(
        published_date__year=timezone.now().year
    ).values('published_date__month').annotate(
        count=Count('id')
    ).order_by('published_date__month')
    
    comments_by_month = Comment.objects.filter(
        created_date__year=timezone.now().year
    ).values('created_date__month').annotate(
        count=Count('id')
    ).order_by('created_date__month')
    
    # Get branch distribution
    branch_distribution = MilitaryProfile.objects.values('branch').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Get top authors
    top_authors = User.objects.annotate(
        post_count=Count('blog_posts')
    ).order_by('-post_count')[:5]
    
    # Get featured posts
    featured_posts = BlogPost.objects.filter(is_featured=True)
    
    # Get pending comments
    pending_comments = Comment.objects.filter(approved=False).order_by('-created_date')[:10]
    
    context = {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'recent_users': recent_users,
        'posts_by_month': posts_by_month,
        'comments_by_month': comments_by_month,
        'branch_distribution': branch_distribution,
        'top_authors': top_authors,
        'featured_posts': featured_posts,
        'pending_comments': pending_comments,
    }
    
    return render(request, 'adminsx/dashboard.html', context)

# Admin Blog Post Management
@staff_member_required
def admin_post_list(request):
    posts = BlogPost.objects.all().order_by('-created_date')
    
    # Filter by author
    author_id = request.GET.get('author')
    if author_id:
        posts = posts.filter(author_id=author_id)
    
    # Filter by featured status
    featured = request.GET.get('featured')
    if featured:
        is_featured = featured == 'true'
        posts = posts.filter(is_featured=is_featured)
    
    # Filter by published status
    published = request.GET.get('published')
    if published:
        if published == 'true':
            posts = posts.filter(published_date__isnull=False)
        else:
            posts = posts.filter(published_date__isnull=True)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 20)  # 20 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all authors for filter dropdown
    authors = User.objects.filter(blog_posts__isnull=False).distinct()
    
    context = {
        'page_obj': page_obj,
        'authors': authors,
        'current_author': author_id,
        'current_featured': featured,
        'current_published': published,
        'search_query': search_query,
    }
    
    return render(request, 'adminsx/post_list.html', context)

@staff_member_required

def admin_post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all().order_by('-created_date')
    
    approved_count = comments.filter(approved=True).count()
    total_comments = comments.count()
    
    percentage = (approved_count / total_comments) * 100 if total_comments > 0 else 0

    context = {
        'post': post,
        'comments': comments,
        'approved_count': approved_count,
        'percentage': percentage
    }
    
    return render(request, 'adminsx/post_detail.html', context)

@staff_member_required
def admin_post_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('admin_post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    
    context = {
        'form': form,
        'title': 'Create New Post',
    }
    
    return render(request, 'adminsx/post_form.html', context)

@staff_member_required
def admin_post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('admin_post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'title': 'Edit Post',
    }
    
    return render(request, 'adminsx/post_form.html', context)

@staff_member_required
@require_POST
def admin_post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    messages.success(request, 'Post deleted successfully!')
    return redirect('admin_post_list')

@staff_member_required
@require_POST
def admin_post_feature(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.is_featured = not post.is_featured
    post.save()
    
    if post.is_featured:
        messages.success(request, 'Post added to featured!')
    else:
        messages.success(request, 'Post removed from featured!')
    
    return redirect('admin_post_detail', pk=post.pk)

@staff_member_required
@require_POST
def admin_post_publish(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if post.published_date:
        post.published_date = None
        message = 'Post unpublished successfully!'
    else:
        post.published_date = timezone.now()
        message = 'Post published successfully!'
    
    post.save()
    messages.success(request, message)
    return redirect('admin_post_detail', pk=post.pk)

@staff_member_required
def admin_post_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=blog_posts_{timezone.now().strftime("%Y%m%d")}.csv'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Author', 'Created Date', 'Published Date', 'Featured', 'Comment Count'])
    
    posts = BlogPost.objects.all().annotate(comment_count=Count('comments'))
    
    for post in posts:
        writer.writerow([
            post.id,
            post.title,
            post.author.username,
            post.created_date,
            post.published_date,
            'Yes' if post.is_featured else 'No',
            post.comment_count
        ])
    
    return response

# Admin Comment Management
@staff_member_required
def admin_comment_list(request):
    comments = Comment.objects.all().order_by('-created_date')
    
    # Filter by approval status
    approved = request.GET.get('approved')
    if approved:
        is_approved = approved == 'true'
        comments = comments.filter(approved=is_approved)
    
    # Filter by post
    post_id = request.GET.get('post')
    if post_id:
        comments = comments.filter(post_id=post_id)
    
    # Filter by author
    author_id = request.GET.get('author')
    if author_id:
        comments = comments.filter(author_id=author_id)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        comments = comments.filter(
            Q(text__icontains=search_query) | 
            Q(author__username__icontains=search_query) |
            Q(post__title__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(comments, 50)  # 50 comments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all posts and authors for filter dropdowns
    posts = BlogPost.objects.all()
    authors = User.objects.filter(comments__isnull=False).distinct()
    
    context = {
        'page_obj': page_obj,
        'posts': posts,
        'authors': authors,
        'current_approved': approved,
        'current_post': post_id,
        'current_author': author_id,
        'search_query': search_query,
    }
    
    return render(request, 'adminsx/comment_list.html', context)

@staff_member_required
def admin_comment_detail(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    context = {
        'comment': comment,
    }
    
    return render(request, 'adminsx/comment_detail.html', context)

@staff_member_required
def admin_comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('admin_comment_detail', pk=comment.pk)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment,
        'title': 'Edit Comment',
    }
    
    return render(request, 'adminsx/comment_form.html', context)

@staff_member_required
@require_POST
def admin_comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('admin_post_detail', pk=post_pk)

@staff_member_required
@require_POST
def admin_comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approved = not comment.approved
    comment.save()
    
    if comment.approved:
        messages.success(request, 'Comment approved!')
    else:
        messages.success(request, 'Comment unapproved!')
    
    return redirect('admin_comment_detail', pk=comment.pk)

@staff_member_required
def admin_comment_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=comments_{timezone.now().strftime("%Y%m%d")}.csv'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Post', 'Author', 'Created Date', 'Approved', 'Text'])
    
    comments = Comment.objects.all()
    
    for comment in comments:
        writer.writerow([
            comment.id,
            comment.post.title,
            comment.author.username,
            comment.created_date,
            'Yes' if comment.approved else 'No',
            comment.text
        ])
    
    return response

@staff_member_required
@require_POST
def admin_bulk_approve_comments(request):
    comment_ids = request.POST.getlist('comment_ids')
    Comment.objects.filter(id__in=comment_ids).update(approved=True)
    messages.success(request, f'{len(comment_ids)} comments approved successfully!')
    return redirect('admin_comment_list')

@staff_member_required
@require_POST
def admin_bulk_disapprove_comments(request):
    comment_ids = request.POST.getlist('comment_ids')
    Comment.objects.filter(id__in=comment_ids).update(approved=False)
    messages.success(request, f'{len(comment_ids)} comments unapproved successfully!')
    return redirect('admin_comment_list')

# Admin User Management
@user_passes_test(is_superuser)
def admin_user_list(request):
    users = User.objects.all().order_by('-date_joined')
    
    # Filter by staff status
    is_staff = request.GET.get('staff')
    if is_staff:
        is_staff_bool = is_staff == 'true'
        users = users.filter(is_staff=is_staff_bool)
    
    # Filter by active status
    is_active = request.GET.get('active')
    if is_active:
        is_active_bool = is_active == 'true'
        users = users.filter(is_active=is_active_bool)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users, 20)  # 20 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'current_staff': is_staff,
        'current_active': is_active,
        'search_query': search_query,
    }
    
    return render(request, 'adminsx/user_list.html', context)

@user_passes_test(is_superuser)
def admin_user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    try:
        profile = user.militaryprofile
    except MilitaryProfile.DoesNotExist:
        profile = None
    
    posts = user.blog_posts.all().order_by('-created_date')
    comments = user.comments.all().order_by('-created_date')
    
    context = {
        'user_obj': user,  # Using user_obj to avoid conflict with request.user
        'profile': profile,
        'posts': posts,
        'comments': comments,
    }
    
    return render(request, 'adminsx/user_detail.html', context)

@user_passes_test(is_superuser)
@require_POST
def admin_user_toggle_staff(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_staff = not user.is_staff
    user.save()
    
    if user.is_staff:
        messages.success(request, f'{user.username} is now a staff member!')
    else:
        messages.success(request, f'{user.username} is no longer a staff member!')
    
    return redirect('admin_user_detail', pk=user.pk)

@user_passes_test(is_superuser)
@require_POST
def admin_user_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    
    if user.is_active:
        messages.success(request, f'{user.username} is now active!')
    else:
        messages.success(request, f'{user.username} is now inactive!')
    
    return redirect('admin_user_detail', pk=user.pk)

@user_passes_test(is_superuser)
def admin_user_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=users_{timezone.now().strftime("%Y%m%d")}.csv'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Username', 'Email', 'First Name', 'Last Name', 'Date Joined', 'Last Login', 'Active', 'Staff', 'Superuser'])
    
    users = User.objects.all()
    
    for user in users:
        writer.writerow([
            user.id,
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.date_joined,
            user.last_login,
            'Yes' if user.is_active else 'No',
            'Yes' if user.is_staff else 'No',
            'Yes' if user.is_superuser else 'No'
        ])
    
    return response

# Admin Profile Management
@staff_member_required
def admin_profile_list(request):
    profiles = MilitaryProfile.objects.all().order_by('user__username')
    
    # Filter by branch
    branch = request.GET.get('branch')
    if branch:
        profiles = profiles.filter(branch=branch)
    
    # Filter by years of service
    years = request.GET.get('years')
    if years:
        try:
            years_int = int(years)
            profiles = profiles.filter(years_of_service=years_int)
        except ValueError:
            pass
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        profiles = profiles.filter(
            Q(user__username__icontains=search_query) | 
            Q(user__email__icontains=search_query) |
            Q(rank__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(profiles, 20)  # 20 profiles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get branch choices for filter dropdown
    branch_choices = MilitaryProfile._meta.get_field('branch').choices
    
    context = {
        'page_obj': page_obj,
        'branch_choices': branch_choices,
        'current_branch': branch,
        'current_years': years,
        'search_query': search_query,
    }
    
    return render(request, 'adminsx/profile_list.html', context)

@staff_member_required
def admin_profile_detail(request, pk):
    profile = get_object_or_404(MilitaryProfile, pk=pk)
    
    context = {
        'profile': profile,
    }
    
    return render(request, 'adminsx/profile_detail.html', context)

@staff_member_required
def admin_profile_edit(request, pk):
    profile = get_object_or_404(MilitaryProfile, pk=pk)
    
    if request.method == 'POST':
        form = MilitaryProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('admin_profile_detail', pk=profile.pk)
    else:
        form = MilitaryProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'title': 'Edit Profile',
    }
    
    return render(request, 'adminsx/profile_form.html', context)

@staff_member_required
def admin_profile_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=profiles_{timezone.now().strftime("%Y%m%d")}.csv'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Username', 'Email', 'Branch', 'Rank', 'Years of Service', 'Post Count', 'Comment Count'])
    
    profiles = MilitaryProfile.objects.all().select_related('user')
    
    for profile in profiles:
        writer.writerow([
            profile.id,
            profile.user.username,
            profile.user.email,
            profile.get_branch_display(),
            profile.rank,
            profile.years_of_service,
            profile.user.blog_posts.count(),
            profile.user.comments.count()
        ])
    
    return response

# Admin Statistics and Reports
@staff_member_required
def admin_statistics(request):
    # Time period filter
    period = request.GET.get('period', 'month')
    
    if period == 'week':
        start_date = timezone.now() - timedelta(days=7)
    elif period == 'month':
        start_date = timezone.now() - timedelta(days=30)
    elif period == 'year':
        start_date = timezone.now() - timedelta(days=365)
    else:  # all time
        start_date = None
    
    # Base querysets
    posts_qs = BlogPost.objects
    comments_qs = Comment.objects
    users_qs = User.objects
    
    if start_date:
        posts_qs = posts_qs.filter(created_date__gte=start_date)
        comments_qs = comments_qs.filter(created_date__gte=start_date)
        users_qs = users_qs.filter(date_joined__gte=start_date)
    
    # Post statistics
    total_posts = posts_qs.count()
    published_posts = posts_qs.filter(published_date__isnull=False).count()
    featured_posts = posts_qs.filter(is_featured=True).count()
    
    # Comment statistics
    total_comments = comments_qs.count()
    approved_comments = comments_qs.filter(approved=True).count()
    
    # User statistics
    total_users = users_qs.count()
    active_users = users_qs.filter(is_active=True).count()
    staff_users = users_qs.filter(is_staff=True).count()
    
    # Posts by branch
    posts_by_branch = BlogPost.objects.filter(
        author__militaryprofile__isnull=False
    ).values(
        'author__militaryprofile__branch'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Posts by month
    posts_by_month = []
    comments_by_month = []
    
    # Get the last 12 months
    for i in range(11, -1, -1):
        month_start = timezone.now() - timedelta(days=30 * i)
        month_end = timezone.now() - timedelta(days=30 * (i - 1)) if i > 0 else timezone.now()
        
        month_posts = BlogPost.objects.filter(
            created_date__gte=month_start,
            created_date__lt=month_end
        ).count()
        
        month_comments = Comment.objects.filter(
            created_date__gte=month_start,
            created_date__lt=month_end
        ).count()
        
        posts_by_month.append({
            'month': month_start.strftime('%b %Y'),
            'count': month_posts
        })
        
        comments_by_month.append({
            'month': month_start.strftime('%b %Y'),
            'count': month_comments
        })
    
    context = {
        'period': period,
        'total_posts': total_posts,
        'published_posts': published_posts,
        'featured_posts': featured_posts,
        'total_comments': total_comments,
        'approved_comments': approved_comments,
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'posts_by_branch': posts_by_branch,
        'posts_by_month': posts_by_month,
        'comments_by_month': comments_by_month,
    }
    
    return render(request, 'adminsx/statistics.html', context)

@staff_member_required
def admin_activity_log(request):
    # This would typically use Django's admin log
    from django.contrib.admin.models import LogEntry
    
    logs = LogEntry.objects.all().select_related('content_type', 'user').order_by('-action_time')
    
    # Pagination
    paginator = Paginator(logs, 50)  # 50 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'adminsx/activity_log.html', context)

# AJAX endpoints for admin
@staff_member_required
def admin_ajax_post_stats(request):
    # Get post statistics for charts
    posts_by_day = []
    
    # Get the last 30 days
    for i in range(29, -1, -1):
        day = timezone.now() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        day_posts = BlogPost.objects.filter(
            created_date__gte=day_start,
            created_date__lte=day_end
        ).count()
        
        posts_by_day.append({
            'date': day.strftime('%Y-%m-%d'),
            'count': day_posts
        })
    
    return JsonResponse({
        'posts_by_day': posts_by_day
    })

@staff_member_required
def admin_ajax_comment_stats(request):
    # Get comment statistics for charts
    comments_by_day = []
    
    # Get the last 30 days
    for i in range(29, -1, -1):
        day = timezone.now() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        day_comments = Comment.objects.filter(
            created_date__gte=day_start,
            created_date__lte=day_end
        ).count()
        
        comments_by_day.append({
            'date': day.strftime('%Y-%m-%d'),
            'count': day_comments
        })
    
    return JsonResponse({
        'comments_by_day': comments_by_day
    })

@staff_member_required
def admin_ajax_user_stats(request):
    # Get user statistics for charts
    users_by_day = []
    
    # Get the last 30 days
    for i in range(29, -1, -1):
        day = timezone.now() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        day_users = User.objects.filter(
            date_joined__gte=day_start,
            date_joined__lte=day_end
        ).count()
        
        users_by_day.append({
            'date': day.strftime('%Y-%m-%d'),
            'count': day_users
        })
    
    return JsonResponse({
        'users_by_day': users_by_day
    })

# Regular views (non-admin)
def home(request):
    featured_posts = BlogPost.objects.filter(is_featured=True, published_date__isnull=False).order_by('-published_date')[:5]
    recent_posts = BlogPost.objects.filter(published_date__isnull=False).order_by('-published_date')[:10]
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
    }
    
    return render(request, 'blog/home.html', context)

def blog_list(request):
    posts = BlogPost.objects.filter(published_date__isnull=False).order_by('-published_date')
    
    # Filter by branch
    branch = request.GET.get('branch')
    if branch:
        posts = posts.filter(author__militaryprofile__branch=branch)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get branch choices for filter dropdown
    from .models import MilitaryProfile
    branch_choices = MilitaryProfile._meta.get_field('branch').choices
    
    context = {
        'page_obj': page_obj,
        'branch_choices': branch_choices,
        'current_branch': branch,
        'search_query': search_query,
    }
    
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published_date__isnull=False)
    comments = post.comments.filter(approved=True).order_by('-created_date')
    
    # Increment view count
    post.views = post.views + 1
    post.save(update_fields=['views'])
    
    # Comment form
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
            return redirect('blog_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    
    return render(request, 'blog/blog_detail.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogPostForm()
    
    context = {
        'form': form,
        'title': 'Create New Post',
    }
    
    return render(request, 'blog/post_form.html', context)

@login_required
def edit_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Check if the user is the author or staff
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('blog_detail', slug=post.slug)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'title': 'Edit Post',
    }
    
    return render(request, 'blog/post_form.html', context)

@login_required
def delete_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    # Check if the user is the author or staff
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('blog_detail', slug=post.slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted!')
        return redirect('blog_list')
    
    context = {
        'post': post,
    }
    
    return render(request, 'blog/post_confirm_delete.html', context)

@login_required
def profile(request):
    try:
        profile = request.user.militaryprofile
    except MilitaryProfile.DoesNotExist:
        profile = MilitaryProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = MilitaryProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = MilitaryProfileForm(instance=profile)
    
    # Get user's posts
    posts = request.user.blog_posts.all().order_by('-created_date')
    
    context = {
        'profile': profile,
        'form': form,
        'posts': posts,
    }
    
    return render(request, 'blog/profile.html', context)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    
    try:
        profile = user.militaryprofile
    except MilitaryProfile.DoesNotExist:
        profile = None
    
    # Get user's public posts
    posts = user.blog_posts.filter(published_date__isnull=False).order_by('-published_date')
    
    context = {
        'profile_user': user,  # Using profile_user to avoid conflict with request.user
        'profile': profile,
        'posts': posts,
    }
    
    return render(request, 'blog/user_profile.html', context)

# Debug view for URL patterns
def debug_urls(request):
    """A simple view to debug URL configurations."""
    from django.urls import get_resolver
    resolver = get_resolver()
    url_patterns = sorted([
        (key, value[0][0][0])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, str)
    ])

    html = "<h1>URL Patterns</h1><ul>"
    for name, pattern in url_patterns:
        html += f"<li><strong>{name}</strong>: {pattern}</li>"
    html += "</ul>"

    return HttpResponse(html)




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app.models import Personnel, Country
from app.forms import PersonnelForm, AchievementFormSet

def phome(request):
    personnel_list = Personnel.objects.all()
    countries = Country.objects.all()
    
    # Filter by country if specified
    country_id = request.GET.get('country')
    if country_id:
        personnel_list = personnel_list.filter(country_id=country_id)
    
    context = {
        'personnel_list': personnel_list,
        'countries': countries,
        'selected_country': country_id
    }
    return render(request, 'adminsx/phone.html', context)

def personnel_detail(request, pk):
    person = get_object_or_404(Personnel, pk=pk)
    achievements = person.achievements.all().order_by('-date')
    awards = person.awards.all()
    
    context = {
        'person': person,
        'achievements': achievements,
        'awards': awards
    }
    return render(request, 'adminsx/pdetail.html', context)

@login_required
def personnel_create(request):
    if request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES)
        achievement_formset = AchievementFormSet(request.POST, prefix='achievements')
        
        if form.is_valid() and achievement_formset.is_valid():
            # Save the personnel record
            person = form.save()
            
            # Save the achievements
            achievements = achievement_formset.save(commit=False)
            for achievement in achievements:
                achievement.personnel = person
                achievement.save()
            
            # Handle deleted achievements
            for obj in achievement_formset.deleted_objects:
                obj.delete()
                
            messages.success(request, f"Personnel record for {person.first_name} {person.last_name} created successfully!")
            return redirect('personnel_detail', pk=person.pk)
    else:
        form = PersonnelForm()
        achievement_formset = AchievementFormSet(prefix='achievements')
    
    context = {
        'form': form,
        'achievement_formset': achievement_formset,
        'title': 'Create New Personnel Record',
        'button_text': 'Create Record'
    }
    return render(request, 'adminsx/personeal.html', context)

@login_required
def personnel_update(request, pk):
    person = get_object_or_404(Personnel, pk=pk)
    
    if request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES, instance=person)
        achievement_formset = AchievementFormSet(request.POST, instance=person, prefix='achievements')
        
        if form.is_valid() and achievement_formset.is_valid():
            # Save the personnel record
            person = form.save()
            
            # Save the achievements
            achievements = achievement_formset.save(commit=False)
            for achievement in achievements:
                achievement.personnel = person
                achievement.save()
            
            # Handle deleted achievements
            for obj in achievement_formset.deleted_objects:
                obj.delete()
                
            messages.success(request, f"Personnel record for {person.first_name} {person.last_name} updated successfully!")
            return redirect('personnel_detail', pk=person.pk)
    else:
        form = PersonnelForm(instance=person)
        achievement_formset = AchievementFormSet(instance=person, prefix='achievements')
    
    context = {
        'form': form,
        'achievement_formset': achievement_formset,
        'person': person,
        'title': f'Update Record: {person.rank} {person.first_name} {person.last_name}',
        'button_text': 'Update Record'
    }
    return render(request, 'adminsx/personeal.htmll', context)

@login_required
def personnel_delete(request, pk):
    person = get_object_or_404(Personnel, pk=pk)
    
    if request.method == 'POST':
        person_name = f"{person.first_name} {person.last_name}"
        person.delete()
        messages.success(request, f"Personnel record for {person_name} deleted successfully!")
        return redirect('home')
    
    context = {
        'person': person
    }
    return render(request, 'adminsx/maps.html', context)    