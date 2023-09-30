from habits.apps import HabitsConfig
from django.urls import path
from habits.views import *

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('habits/', HabitListAPIView.as_view(), name='habit_list'),
    path('habits/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_get'),
    path('habits/update/<int:pk>/', HabitsUpdateAPIView.as_view(), name='habits_update'),
    path('habits/delete/<int:pk>/', HabitsDestroyAPIView.as_view(), name='habits_delete'),
    path('user_habits/', HabitUserListAPIView.as_view(), name='user_habits_list')
]
