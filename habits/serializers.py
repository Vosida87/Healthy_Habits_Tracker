from rest_framework import serializers
from habits.models import Habit
from habits.validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """Serializer для привычек"""
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, instance):
        """Для валидации"""
        HabitValidator(instance)(instance)
        return instance
