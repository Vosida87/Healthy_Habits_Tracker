from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    """
    PageNumberPagination - разбивает данные на страницы
    """
    page_size = 5  # Выводим по 5 привычек
