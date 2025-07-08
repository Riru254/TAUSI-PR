from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("nationality", "profile_pic")
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": ("nationality", "profile_pic")
        }),
    )

    list_display = ['username', 'email', 'nationality', 'is_staff']
    list_filter = ['nationality', 'is_staff', 'is_superuser']

admin.site.register(CustomUser, CustomUserAdmin)