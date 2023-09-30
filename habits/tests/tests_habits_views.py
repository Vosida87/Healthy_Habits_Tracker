from rest_framework.test import APITestCase
from habits.models import Habit
from rest_framework.reverse import reverse
from rest_framework import status


class HabitsTestCase(APITestCase):
    """Тесы для привычек по status.HTTP"""
    def setUp(self):
        """Данные для теста"""
        # создаём нового пользователя, отправив запрос к конечной точке djoser
        self.user = self.client.post('/auth/users/', data={'username': 'mario', 'password': 'i-keep-jumping'})
        # получаем веб-токен JSON для вновь созданного пользователя
        response = self.client.post('/auth/jwt/create/', data={'username': 'mario', 'password': 'i-keep-jumping'})
        self.token = response.data['access']
        self.api_authentication()
        self.habit_data = {"place": "test", "time": "2023-09-30", "action": "testing"}

    def api_authentication(self):
        """Добавляем Authorization в Headers"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)

    def test_create_habit(self):
        """Тест на создание привычки"""
        url = reverse('habits:habit_create')
        response = self.client.post(url, data=self.habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_habit(self):
        """Тест на просмотр привычек"""
        url = reverse('habits:habit_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_habit(self):
        """Тест на просмотр привычки"""
        habit = Habit.objects.create(place='place for retrieve', time='2018-09-30', action='test api retrieve')
        url = reverse('habits:habit_get', kwargs={'pk': habit.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_habit(self):
        """Тест на обновление привычки"""
        # создаём привычку от тестового пользователя так как
        # только он может редактировать её
        url = reverse('habits:habit_create')
        response = self.client.post(url, data=self.habit_data)
        updated_habit = {'place': 'place for update', 'action': 'test api update'}
        url = reverse('habits:habits_update', kwargs={'pk': response.data['id']})
        response = self.client.patch(url, data=updated_habit)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_habit(self):
        """Тест на удаление привычки"""
        url = reverse('habits:habit_create')
        response = self.client.post(url, data=self.habit_data)
        url = reverse('habits:habits_delete', kwargs={'pk': response.data['id']})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_user_habits(self):
        """Тест на просмотр привычек пользователя"""
        url = reverse('habits:user_habits_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
