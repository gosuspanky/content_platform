# Paid content platform

Этот проект представляет собой платформу контента, позволяющую пользователям публиковать записи.</br>
Публикации могут быть как бесплатными, так и платными. </br>
Публикации доступны только авторизованным пользователям, которые оплатили разовую подписку через сервис Stripe.</br>
Регистрация пользователей осуществляется по номеру телефона.

## **Стек Технологий:**

<li>Python
<li>Django
<li>Docker
<li>PostgreSQL
<li>Redis
<li>Stripe

## **Структура проекта:**

<li>blog - приложение блога
<li>config - настройки проекта
<li>media - папка для хранения медиафайлов
<li>static - шаблоны/стили
<li>subsciptions - приложение подписок
<li>users - приложение пользователей

## Установка и Запуск

### Шаг 1: Клонировать репозиторий

```bash
git clone https://github.com/IKazzakov/paid_content_platform.git
```
```bash
cd paid_content_platform
```
### Шаг 2: Создать и активировать виртуальное окружение.

__Для работы с переменными окружениями необходимо создать файл `.env`(для локального запуска) и `.env.docker`(для docker compose) заполнить его согласно файлу `.env.sample`:__
```
SECRET_KEY=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=

STRIPE_SECRET_KEY=
STRIPE_PUBLIC_KEY=

CACHE_ENABLED=
CACHE_LOCATION=
```
## Шаг 3: Установить зависимости

```
pip install -r requirements.txt
```
## Шаг 4: Применить миграции
```
python3 manage.py migrate
```
##  Шаг 5: При необходимости для заполнения БД запустить команду:
```
python3 manage.py fill
```
## Шаг 6: Настройка Stripe
__Зарегистрируйтесь на Stripe и получите API ключи.
Укажите их в файле settings.py.__
```
STRIPE_PUBLIC_KEY = 'your_public_key'
STRIPE_SECRET_KEY = 'your_secret_key'
```
## Шаг 7: Запустить сервер
```
python3 manage.py runserver
```
- Доступно по адресу http://localhost:8000

## Тестирование

- Для запуска тестов:

```
python manage.py test
```

## Покрытие кода тестами

- Запуск:

```
coverage run --source='.' manage.py test
```

```
coverage report
```
## Docker
- для начала установите и настройте `docker desktop`. Создайте отдельный файл `.env.docker` и пропишите там свои настройки. Смотрите шаблон `.env.sample`:

### Сборка образа и запуск в фоне после успешной сборки
```
docker-compose up -d —build
```
- для остановки
```
docker-compose down
```




