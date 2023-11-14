from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email')  # Update with existing attributes in your model

admin.site.register(CustomUser, CustomUserAdmin)
