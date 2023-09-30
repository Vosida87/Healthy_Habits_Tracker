from rest_framework.serializers import ValidationError
from habits.models import Habit


class HabitValidator:
    """Валидация для привычек"""
    def __init__(self, instance):
        """Сохраняем поля экземпляра для проверок"""
        self.award = instance.get('award')
        self.related_habit = instance.get('related_habit')
        self.time_to_execute = instance.get('time_to_execute')
        self.is_a_pleasant_habit = instance.get('is_a_pleasant_habit')

    def __call__(self, value):
        if self.award and self.related_habit:
            raise ValidationError('Невозможен одновременный выбор связанной привычки и указания вознаграждения')

        if self.time_to_execute:  # Если значение не None
            if self.time_to_execute > 120:
                raise ValidationError('Время выполнения должно быть не больше 120 секунд')

        if self.related_habit:  # Если значение не None
            pleasant_habits = Habit.objects.filter(is_a_pleasant_habit=True)
            if self.related_habit not in pleasant_habits:
                raise ValidationError('В связанные привычки могут попадать только'
                                      ' привычки с признаком приятной привычки')

        if self.is_a_pleasant_habit and self.award:
            raise ValidationError('У приятной привычки не может быть вознаграждения')
        elif self.is_a_pleasant_habit and self.related_habit:
            raise ValidationError('У приятной привычки не может быть связанной привычки')
