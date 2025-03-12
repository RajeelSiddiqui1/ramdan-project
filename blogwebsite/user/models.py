from django.db import models
from admin_side.models import Admin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class SimpleUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'age']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk:  # Ensure regular user by default on creation
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)


class Creator(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    bio = models.CharField(max_length=255)
    education = models.CharField(max_length=128)
    country = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=13)
    password = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='creator/',null=True,blank=True)
    background_photo = models.ImageField(upload_to='creator_background/',null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.name



class Categories(models.Model):
    name = models.CharField(max_length=65, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Blog(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    )
    name = models.CharField(max_length=65)
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True, related_name="blogs")
    Admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(Creator, on_delete=models.CASCADE, null=True, blank=True)  # Replace SimpleUser with your actual user model
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Fixed from approved BooleanField
    is_deleted = models.BooleanField(default=False)  # Added for soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

    def increase_views(self):
        self.views_count += 1
        self.save(update_fields=["views_count"])



class BlogRead(models.Model):
    user = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, null=True, blank=True, related_name="reads")
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, null=True, blank=True, related_name="creator_reads")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="reads")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog')

    def __str__(self):
        return f"{self.user} read {self.blog}"


class Follow(models.Model):
    follower = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')


class ContactUs(models.Model):
     STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    )
     email = models.EmailField(max_length=100)
     phone_number = models.CharField(max_length=13)
     issue = models.CharField(max_length=100)
     problem = models.CharField(max_length=255)
     user = models.ForeignKey(SimpleUser,on_delete=models.CASCADE,name='user')
     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str__(self):
        return self.issue
    