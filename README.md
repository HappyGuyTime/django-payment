# Проект Django Payment

Этот проект представляет собой веб-приложение, разработанное на Django, для обработки платежей.

## Запуск проекта в Docker

Для запуска проекта вам потребуется Docker и Docker Compose.

1. **Клонирование репозитория:**

    ```bash
    git clone https://github.com/happyguytime/django-payment.git
    cd django-payment
    ```

2. **Настройка переменных окружения:**

    Создайте файл `.env` в корневой директории проекта и укажите следующие переменные окружения:

    ```
    DJANGO_SECRET_KEY=your_django_secret_key
    DJANGO_STRIPE_SECRET_KEY=your_stripe_secret_key
    DJANGO_DEBUG=False
    DJANGO_ALLOWED_HOSTS=your_domain.com
    ```

3. **Сборка и запуск Docker контейнера:**

    Запустите команды:

    ```bash
    docker build -t django-payment-image .
    docker run -d -p 8000:8000 --name django-payment django-payment-image
    ```

    Это создаст Docker-контейнер, установит все зависимости и запустит приложение на порту 8000.

4. **Создание суперпользователя:**

    Запустите контейнер и выполните следующую команду для создания суперпользователя Django:

    ```bash
    docker exec -it django-payment python manage.py createsuperuser
    ```

    Следуйте инструкциям для создания суперпользователя (администратора) в приложении.

5. **Использование административной панели Django:**

    Откройте веб-браузер и перейдите по адресу `http://localhost:8000/admin/`, войдите, используя созданные учетные данные суперпользователя.

6. **Создаем данные для теста приложения:**

    Создайте Discount, Tax, Item, Order

7. **Остановка приложения:**

    Для остановки контейнера выполните:

    ```bash
    docker-compose down
    ```

## Структура проекта

- `config/`: Директория с настройками Django.
- `payment/`: Основная директория приложения.
- `requirements.txt`: Файл с зависимостями Python.

## Дополнительная информация

В проекте используются следующие технологии и библиотеки:

- Python 3.12
- Django
- Stripe API
- Gunicorn
- Docker, Docker Compose