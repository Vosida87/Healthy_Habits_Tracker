from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserProfile
from accounts.permissions import IsOwnerProfileOrReadOnly
from accounts.serializers import UserProfileSerializer


class UserProfileListCreateView(ListCreateAPIView):
    """Миксин из создания и отображения (включает get и post)"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    """Миксин retrieve, update, destroy (get, put, patch, delete)"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]
