from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    
    model = CustomUser
    
    list_display = ['username', 'email', 'mobile_number']
    
    

admin.site.register(CustomUser, CustomUserAdmin)