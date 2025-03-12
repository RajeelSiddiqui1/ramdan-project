from django.contrib import admin
from .models import Categories,Blog, SimpleUser

# Register your models here.
admin.site.register(Categories)
admin.site.register(Blog)
admin.site.register(SimpleUser)