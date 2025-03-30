from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from app.models import BlogPost, Comment, MilitaryProfile

class AdminBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 20, 'cols': 80}),
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 100:
            raise forms.ValidationError("Content must be at least 100 characters long.")
        return content

class AdminCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'cols': 80}),
        }
    
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 5:
            raise forms.ValidationError("Comment must be at least 5 characters long.")
        return text

class AdminMilitaryProfileForm(forms.ModelForm):
    class Meta:
        model = MilitaryProfile
        fields = '__all__'
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5, 'cols': 80}),
        }
    
    def clean_years_of_service(self):
        years = self.cleaned_data.get('years_of_service')
        if years < 0 or years > 50:
            raise forms.ValidationError("Years of service must be between 0 and 50.")
        return years

class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create a military profile for the user
            MilitaryProfile.objects.create(user=user)
        return user

class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')