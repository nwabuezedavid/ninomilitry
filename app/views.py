from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from .models import *
from .forms import UserRegistrationForm, MilitaryProfileForm, BlogPostForm, CommentForm
from .new import *
def home(request):
    featured_posts = BlogPost.objects.filter(is_featured=True, published_date__lte=timezone.now()).order_by('-published_date')[:3]
    recent_posts = BlogPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
    fetch_and_save_military_news()
    personnel_list = Personnel.objects.all()[:6]
    countries = Country.objects.all()
    # Filter by country if specified
    country_id = request.GET.get('country')
    name = request.GET.get('name')

    if country_id  :
        personnel_list = personnel_list.filter(country_id=country_id)
    
    if   name:
        if personnel_list.filter(first_name=name).exists():
            personnel_list = personnel_list.filter(first_name=name)
        if personnel_list.filter(last_name=name).exists():
        
            personnel_list = personnel_list.filter(last_name=first_name)
    
    
    return render(request, './home.html', {
        'personnel_list': personnel_list,
        'countries': countries,
        'selected_country': country_id,
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
    })

def blog_list(request):
    posts = BlogPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    return render(request, './bloglist.html', {'posts': posts, 'query': query})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published_date__lte=timezone.now())
    comments = post.comments.filter(approved=True).order_by('-created_date')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blodetail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = MilitaryProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid() :
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            eee, created = Rank.objects.get_or_create(name=profile.rank)
            print(eee.name)
            w = Personnel.objects.create(
                first_name=profile.user.first_name,
            last_name = profile.user.last_name,
            rank=eee,
            years_of_service=profile.years_of_service,
            biography=profile.bio,
            url =profile.profile_image.url )
            w.save()
            authenticate(request, username=user.username, password=user.password)
            dd= User.objects.get(id=user.id)
            login(request, dd)
            messages.success(request, 'Registration successful! Welcome to the NATO MILITARY.')
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = MilitaryProfileForm()
    
    return render(request, './register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def profile(request):
    try:
        profile = request.user.militaryprofile
    except MilitaryProfile.DoesNotExist:
        profile = MilitaryProfile(user=request.user)
        profile.save()
    
    user_posts = BlogPost.objects.filter(author=request.user).order_by('-created_date')
    
    if request.method == 'POST':
        profile_form = MilitaryProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        profile_form = MilitaryProfileForm(instance=profile)
    
    return render(request, './profile.html', {
        'profile_form': profile_form,
        'user_posts': user_posts,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, 'Your blog post has been published!')
            return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogPostForm()
    
    return render(request, './post.html', {'form': form, 'action': 'Create'})

@login_required
def edit_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Your blog post has been updated!')
            return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, './post.html', {'form': form, 'action': 'Edit'})

def search(request):
    query = request.GET.get('q', '')
    
    if query:
        # Search for posts
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).filter(published_date__lte=timezone.now()).order_by('-published_date')
        
        # Search for authors/profiles
        authors = MilitaryProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(rank__icontains=query) |
            Q(branch__icontains=query) |
            Q(bio__icontains=query)
        )
        
        # Search for comments
        comments = Comment.objects.filter(
            Q(text__icontains=query) |
            Q(author__username__icontains=query)
        ).filter(approved=True).order_by('-created_date')
    else:
        posts = BlogPost.objects.none()
        authors = MilitaryProfile.objects.none()
        comments = Comment.objects.none()
    
    return render(request, './search.html', {
        'query': query,
        'posts': posts,
        'authors': authors,
        'comments': comments,
    })



def blog_list(request):
    posts_list = BlogPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    query = request.GET.get('q')
    
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(posts_list, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    return render(request, './bloglist.html', {
        'posts': posts,
        'query': query,
    })        




def about(request):
    return render(request, "./about.html")

def logoutuser(request):
    logout(request)
    return render(request, "./logout.html")

# from .data import create_initial_data
def personnel(request):
    personnel_list = Personnel.objects.all()
    countries = Country.objects.all()
    # create_initial_data()
    # Filter by country if specified
    country_id = request.GET.get('country')
     
    name = request.GET.get('name')

    if country_id  :
        personnel_list = personnel_list.filter(country_id=country_id)
    
    if   name:
        if personnel_list.filter(first_name=name).exists():
            personnel_list = personnel_list.filter(first_name=name)
        if personnel_list.filter(last_name=name).exists():
        
            personnel_list = personnel_list.filter(last_name=first_name)
    context = {
        'personnel_list': personnel_list,
        'countries': countries,
        'selected_country': country_id
    }
    return render(request, 'personnel/home.html', context)

def personnel_detailx(request, pk):
    person = get_object_or_404(Personnel, pk=pk)
    achievements = person.achievements.all().order_by('-date')
    awards = person.awards.all()
    
    context = {
        'person': person,
        'achievements': achievements,
        'awards': awards
    }
    return render(request, 'personnel/details.html', context)    




    