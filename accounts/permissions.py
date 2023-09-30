from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsOwnerProfileOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Владелец профиля - единственный, кто может изменить свою информацию."""
        #  проверяем, похож ли запрашивающий пользователь на пользовательское поле объекта
        if request.method in SAFE_METHODS:  # SAFE_METHODS - это GET, OPTIONS и HEAD.
            return True
        return obj.user == request.user
