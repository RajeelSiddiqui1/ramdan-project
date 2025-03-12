from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
from django.contrib.auth.hashers import make_password
from django.db import models

class Admin(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    image = models.ImageField(upload_to='staff_images/', blank=False,null=True)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class BlogCountry(models.Model):
    name = models.CharField(max_length=100)
    country_image = models.ImageField(upload_to='country/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)