from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class MilitaryProfile(models.Model):
    BRANCH_CHOICES = [
        ('army', 'Army'),
        ('navy', 'Navy'),
        ('air_force', 'Air Force'),
        ('marines', 'Marines'),
        ('coast_guard', 'Coast Guard'),
        ('space_force', 'Space Force'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
    rank = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_pics', default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS81CHVRX7-8gRLhhfJ8nJFk2FlOV4gLxabHQ&s')
    years_of_service = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog_images', blank=True, null=True)
    url = models.TextField( blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-published_date']
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # Add this
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


from django.db import models

class Rank(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    names = models.CharField(max_length=100, blank=True, null=True)
    flag = models.ImageField(upload_to='flags/', blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"

class Award(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='awards/', blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Personnel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='personnel/', blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    biography = models.TextField(blank=True, null=True)
    years_of_service = models.PositiveIntegerField(blank=True, null=True)
    service_start_date = models.DateField(blank=True, null=True)
    service_end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    awards = models.ManyToManyField(Award, blank=True)
    
    def __str__(self):
        return f"{self.rank} {self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name_plural = "Personnel"

class Achievement(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    
    def __str__(self):
        return self.title