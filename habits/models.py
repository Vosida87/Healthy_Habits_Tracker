from django.db import models
from django.contrib.auth.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """Модель привычки"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='создатель привычки', **NULLABLE)
    place = models.CharField(max_length=255, verbose_name='место')
    time = models.DateTimeField(verbose_name='время начала выполнения')  # Пример '15.05.2018 09:30'
    action = models.TextField(verbose_name='действие')
    is_a_pleasant_habit = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE)

    class PeriodChoices(models.TextChoices):
        """Выборы для периодичности рассылки"""
        EVERY_ONE = ('раз в день', 'раз в день')
        EVERY_TWO = ('раз в 2 дня', 'раз в 2 дня')
        EVERY_THREE = ('раз в 3 дня', 'раз в 3 дня')
        EVERY_FOUR = ('раз в 4 дня', 'раз в 4 дня')
        EVERY_FIVE = ('раз в 5 дней', 'раз в 5 дней')
        EVERY_SIX = ('раз в 6 дней', 'раз в 6 дней')
        EVERY_SEVEN = ('раз в 7 дней', 'раз в 7 дней')

    periodicity = models.CharField(max_length=50, choices=PeriodChoices.choices,
                                   default=PeriodChoices.EVERY_ONE, verbose_name='периодичность')
    award = models.CharField(max_length=255, verbose_name='вознаграждение', **NULLABLE)
    time_to_execute = models.PositiveSmallIntegerField(verbose_name='время на выполнение', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='признак публичности')

    def set_current_time(self, current_datetime):
        """Для обновления времени"""
        self.time = current_datetime
        self.save()

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'Владелец {self.owner}, действие: {self.action}'
