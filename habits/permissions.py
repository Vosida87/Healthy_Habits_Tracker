from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Проверяет пользователя на владельца"""
    def has_permission(self, request, view):
        return bool(request.user == view.get_object().owner)
