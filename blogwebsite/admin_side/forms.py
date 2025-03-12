# admin_side/forms.py
from django import forms
from .models import Admin, Staff, BlogCountry
from user.models import Categories, Blog

class SignupForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email', 'country', 'age', 'phone_number', 'password', 'image']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StaffEditForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email', 'country', 'age', 'phone_number', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

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


class BlogCountryForm(forms.ModelForm):
    class Meta:
        model = BlogCountry
        fields = ['name','country_image']
        widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Country Name'}),
        'country_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
