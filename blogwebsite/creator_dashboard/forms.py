from django import forms
import re
from user.models import Blog
from .models import Story

class CreatorLoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        required=True,
        error_messages={
            'required': 'Password is required.'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name', 'description', 'category', 'photo']  # Removed 'status', added fields from your model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Blog Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write something only paragraph...', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class BlogStatusForm(forms.Form):
    action = forms.ChoiceField(
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('delete', 'Delete')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )    


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['content','text']
        widgets = {
            'content': forms.FileInput(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write something....'}),
        }
