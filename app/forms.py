from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MilitaryProfile, BlogPost, Comment

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class MilitaryProfileForm(forms.ModelForm):
    class Meta:
        model = MilitaryProfile
        fields = ('branch', 'rank', 'bio', 'profile_image', 'years_of_service')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'slug', 'content', 'featured_image', 'is_featured',"url",)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'editor'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].help_text = "A URL-friendly name for your blog post (e.g., 'my-military-experience')"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }



from django import forms
from .models import Personnel, Achievement, Award

class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = [
            'first_name', 'last_name', 'rank', 'country', 
            'date_of_birth', 'photo', 'biography', 
            'years_of_service', 'service_start_date', 
            'service_end_date', 'is_active', 'awards', "url",
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'service_start_date': forms.DateInput(attrs={'type': 'date'}),
            'service_end_date': forms.DateInput(attrs={'type': 'date'}),
            'biography': forms.Textarea(attrs={'rows': 6}),
            'awards': forms.CheckboxSelectMultiple(),
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'description', 'date', ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

# Form for creating multiple achievements at once
AchievementFormSet = forms.inlineformset_factory(
    Personnel, 
    Achievement, 
    form=AchievementForm, 
    extra=2,  # Number of empty forms to display
    can_delete=True
)        