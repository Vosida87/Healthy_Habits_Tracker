from django.contrib import admin
from accounts.models import UserProfile


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    """Для создания пользователей в админке"""
    list_display = ('user',)
