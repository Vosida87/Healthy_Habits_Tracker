# Трекер полезных привычек

Пользователи могут регистрироваться и создавать свои привычки, а бот в телеграмме будет их уведомлять.

Покрытие тестами 86%

Аутентификация сделана через djoser

# Настройки для запуска проекта (windows)

1. Установите все зависимости командой pip install - r requirements.txt
2. Создайте в проекте файл .env
   Он должен содержать следующие поля:
   - SECRET_KEY='***' ключ вашего джанго
   - TELEGRAM_BOT_API_KEY='***' ваш ключ к боту в телеграмме
  
     
   БД использовалась по умолчанию, но также можно добавить свои настройки, к примеру postgres:

        - DB_ENGINE='django.db.backends.postgresql'
     
        - DB_NAME='<НАЗВАНИЕ ВАШЕЙ БД>'
     
        - DB_USER='ИМЯ ПОЛЬЗОВАТЕЛЯ'
     
        - DB_PASSWORD='<ПАРОЛЬ К БД>'
     
   - CACHE_ENABLED='True'
   - LOCATION="redis://127.0.0.1:6379"

# Запуск проекта

  1.В wsl (ubuntu) устанавливаем и запускаем redis:

Порядок комманд:
  - sudo apt-get update
  - sudo apt-get install redis
  - sudo service redis-server start
  - redis-cli
  - ping


2. Для миграций: python manage.py makemigrations | python manage.py migrate
3. Для запуска проекта: python manage.py runserver 
4. Для запуска celery: celery -A config worker -l INFO -P eventlet
