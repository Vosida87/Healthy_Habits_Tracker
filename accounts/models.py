from django.db import models
from django.contrib.auth.models import User

NULLABLE = {'blank': True, 'null': True}


class UserProfile(models.Model):
    """Расширенная модель пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    description = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    telegram_id = models.IntegerField(verbose_name='Telegram id', **NULLABLE)

    def __str__(self):
        return self.user.username
