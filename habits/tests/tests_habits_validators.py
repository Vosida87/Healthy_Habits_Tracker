from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HabitSerializerValidator(APITestCase):
    """Тесы для validate habits"""
    def setUp(self):
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

    def test_impossibility_of_reward_and_related_habit(self):
        """Невозможно указать и награду и связанную привычку"""
        # Создаём привычку, которая в будущем будет связанной
        url = reverse('habits:habit_create')
        habit_response = self.client.post(url, data=self.habit_data)
        habit_data = habit_response.data
        # Создаём привычку у которой будет и награда и связанная привычка
        data = {"place": "test", "time": "2023-09-30", "action": "testing", "award": "eat donut",
                "related_habit": habit_data['id']}
        # Проверяем
        response = self.client.post(url, data=data)
        expected_response = "{'non_field_errors':" \
                            " [ErrorDetail(string='Невозможен одновременный выбор" \
                            " связанной привычки и указания вознаграждения'," \
                            " code='invalid')]}"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), expected_response)

    def test_limitation_of_time_to_execute(self):
        """Нельзя поставить значение времени на выполнение выше 120"""
        # Создаём привычку с нарушением по ограничению времени
        habit_data = {"place": "test", "time": "2023-09-30", "action": "testing", "time_to_execute": 150}
        url = reverse('habits:habit_create')
        response = self.client.post(url, data=habit_data)
        # Проверяем
        expected_response = "{'non_field_errors':" \
                            " [ErrorDetail(string='Время выполнения должно быть не больше 120 секунд'," \
                            " code='invalid')]}"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), expected_response)

    def test_related_can_only_be_a_pleasant(self):
        """Связанная привычка может быть только приятной привычкой"""
        # Создаём НЕ приятную привычку
        habit_data = {"place": "test", "time": "2023-09-30", "action": "testing", "is_a_pleasant_habit": False}
        url = reverse('habits:habit_create')
        habit_response = self.client.post(url, data=habit_data)
        habit_data = habit_response.data
        # Создаём ту, которая свяжется с НЕ приятной
        data = {"place": "test", "time": "2023-09-30", "action": "testing", "related_habit": habit_data['id']}
        # Проверяем
        response = self.client.post(url, data=data)
        expected_response = "{'non_field_errors': [ErrorDetail(string='В связанные привычки могут попадать только" \
                            " привычки с признаком приятной привычки', code='invalid')]}"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), expected_response)

    def test_pleasant_habit_cannot_be_rewarded(self):
        """Приятная привычка не может вознаграждаться"""
        # Создаём ту которая вознаграждается
        habit_data = {"place": "test", "time": "2023-09-30", "action": "testing",
                      "is_a_pleasant_habit": True, "award": "eat donut"}
        url = reverse('habits:habit_create')
        response = self.client.post(url, data=habit_data)
        expected_response = "{'non_field_errors': [ErrorDetail(string='У приятной привычки" \
                            " не может быть вознаграждения', code='invalid')]}"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), expected_response)

    def test_pleasant_cannot_have_a_related_habit(self):
        """У приятной привычки не может быть связанной привычки"""
        # Создаём ту которая будет связанной (она должна быть приятной)
        habit_data = {"place": "test", "time": "2023-09-30", "action": "testing", "is_a_pleasant_habit": True}
        url = reverse('habits:habit_create')
        habit_response = self.client.post(url, data=habit_data)
        habit_data = habit_response.data
        # Создаём ту, которая свяжется
        data = {"place": "test", "time": "2023-09-30", "action": "testing",
                "related_habit": habit_data['id'], "is_a_pleasant_habit": True}
        response = self.client.post(url, data=data)
        # Проверяем
        expected_response = "{'non_field_errors': [ErrorDetail(string='У приятной привычки " \
                            "не может быть связанной привычки', code='invalid')]}"
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data), expected_response)
