from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserProfileListCreateView, UserProfileDetailView

urlpatterns = [
    # Забирает всех пользователей + создаёт профиль
    path("all-profiles", UserProfileListCreateView.as_view(), name="all-profiles"),
    # Для работы с профилем авторизированного пользователя
    path("profile/<int:pk>", UserProfileDetailView.as_view(), name="profile"),
]
