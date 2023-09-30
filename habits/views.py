from rest_framework import generics
from habits.serializers import HabitSerializer
from habits.models import Habit
from habits.paginators import HabitPaginator
from rest_framework.permissions import IsAuthenticated
from habits.permissions import IsOwner


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание привычки"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Владельцем становиться пользователь"""
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.save()


class HabitListAPIView(generics.ListAPIView):
    """Отображение опубликованных привычек"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def get_queryset(self):
        """Фильтр на публикацию"""
        queryset = Habit.objects.filter(is_published=True)
        return queryset


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Отображение привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()  # для того, чтоб класс понимал с какой выборкой работать


class HabitsUpdateAPIView(generics.UpdateAPIView):
    """Редактирование привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitsDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]


class HabitUserListAPIView(generics.ListAPIView):
    """Отображение привычек пользователя"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтр на пользователя"""
        queryset = Habit.objects.filter(owner=self.request.user)
        return queryset
