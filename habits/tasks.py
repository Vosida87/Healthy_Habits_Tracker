from celery import shared_task
from habits.models import Habit
from datetime import datetime, timedelta
from config.settings import TELEGRAM_BOT_API_KEY
import requests


@shared_task
def send_notify(pk, tg_id):
    """Уведомления для пользователя"""
    habit = Habit.objects.get(pk=pk)  # Получаем привычку по pk
    message = f'Уведомление о действии: {habit.action}, время: {habit.time}, место выполнения: {habit.place}'
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage?chat_id={tg_id}&text={message}"
    return requests.get(url).json()  # Отправляем письмо


@shared_task
def check_if_send_notification():
    """Проверка, нужно ли уведомить пользователя, если да то отправляем сообщение"""
    habits = Habit.objects.all()  # Собираем все привычки
    current_time = datetime.now()  # Берём настоящее время
    formatted_string = current_time.strftime('%Y-%m-%d %H:%M:%S')  # Форматируем в один вид для операторов сравнения
    formatted_datetime = datetime.strptime(formatted_string, '%Y-%m-%d %H:%M:%S')  # Из строки делаем объект datetime
    for habit in habits:
        date_time_from_db = habit.time.strftime('%Y-%m-%d %H:%M:%S')  # Также приводим в нужный вид время из БД
        formatted_date = datetime.strptime(date_time_from_db, '%Y-%m-%d %H:%M:%S')
        if habit.owner.profile.telegram_id:  # Если у пользователя есть telegram id
            if habit.periodicity == 'раз в день':
                if formatted_datetime - formatted_date > timedelta(days=1):
                    send_notify(habit.pk, habit.owner.profile.telegram_id)  # Если проверка пройдена, то уведомляем
                    Habit.set_current_time(habit, formatted_string)  # Обязательно обновим время в БД
            if habit.periodicity == 'раз в 2 дня':
                if formatted_datetime - formatted_date > timedelta(days=2):
                    send_notify(habit.pk, habit.owner.profile.telegram_id)
                    Habit.set_current_time(habit, formatted_string)
            if habit.periodicity == 'раз в 3 дня':
                if formatted_datetime - formatted_date > timedelta(days=3):
                    send_notify(habit.pk, habit.owner.profile.telegram_id)
                    Habit.set_current_time(habit, formatted_string)
            if habit.periodicity == 'раз в 4 дня':
                if formatted_datetime - formatted_date > timedelta(days=4):
                    send_notify(habit.pk, habit.owner.profile.telegram_id)
                    Habit.set_current_time(habit, formatted_string)
            if habit.periodicity == 'раз в 5 дней':
                if formatted_datetime - formatted_date > timedelta(days=5):
                    send_notify(habit.pk, habit.owner.profile.telegram_id)
                    Habit.set_current_time(habit, formatted_string)
            if habit.periodicity == 'раз в 6 дней':
                if formatted_datetime - formatted_date > timedelta(days=6):
                    send_notify(habit.pk, habit.owner.profile.telegram_id)
                    Habit.set_current_time(habit, formatted_string)
            if habit.periodicity == 'раз в 7 дней':
                if formatted_datetime - formatted_date > timedelta(days=7):
                    send_notify(habit.pk, habit.owner.profile.telegram_id)
                    Habit.set_current_time(habit, formatted_string)
