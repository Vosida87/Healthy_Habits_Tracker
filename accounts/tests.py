from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status


class UserProfileTestCase(APITestCase):
    """Тесты для пользователя"""
    profile_list_url = reverse('all-profiles')

    def setUp(self):
        """Данные для теста"""
        # создаём нового пользователя, отправив запрос к конечной точке djoser
        self.user = self.client.post('/auth/users/', data={'username': 'mario', 'password': 'i-keep-jumping'})
        # получаем веб-токен JSON для вновь созданного пользователя
        response = self.client.post('/auth/jwt/create/', data={'username': 'mario', 'password': 'i-keep-jumping'})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        """Добавляем Authorization в Headers"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)

    def test_userprofile_list_authenticated(self):
        """Получить список всех профилей пользователей во время аутентификации пользователя запроса"""
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_userprofile_list_unauthenticated(self):
        """Получить список всех профилей пользователей, пока запрос пользователя не прошел проверку подлинности"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_userprofile_detail_retrieve(self):
        """Проверьте, чтобы получить данные профиля аутентифицированного пользователя"""
        response = self.client.get(reverse('profile', kwargs={'pk': 1}))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_userprofile_profile(self):
        """Заполнить профиль пользователя, который был автоматически создан с использованием сигналов"""
        profile_data = {'description': 'I am a very famous game character', 'location': 'nintendo world',
                        'is_creator': 'true'}
        response = self.client.put(reverse('profile', kwargs={'pk': 1}), data=profile_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_userprofile_delete(self):
        """Удаление профиля пользователя"""
        response = self.client.delete(reverse('profile', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
