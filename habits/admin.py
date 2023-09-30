from django.contrib import admin
from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Для создания привычек в админке"""
    list_display = ('owner', 'action')
