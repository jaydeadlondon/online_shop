# WorldPactLeader - Online Store

Онлайн-магазин нишевой одежды с минималистичным дизайном.

## Быстрый старт

### 1. Установка

```bash
git clone <repository-url>
cd online_shop
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Настройка

Создайте файл `.env` в корне проекта:

```env
# Database (SQLite для быстрого старта)
DB_ENGINE=sqlite3

# Или PostgreSQL
# DB_ENGINE=postgresql
# DB_NAME=your_db_name
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=5432

# Stripe Keys (для тестирования получите на https://stripe.com)
STRIPE_PUBLIC_KEY=pk_test_your_public_key
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Django Secret
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 3. База данных

```bash
python manage.py migrate
python manage.py create_sample_data
```

**Для входа в админку создайте пользователя:**
- Зарегистрируйтесь на сайте: http://localhost:8000/register/
- Или через Django shell:
  ```bash
  python manage.py shell
  >>> from users.models import User
  >>> User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
  >>> exit()
  ```

### 4. Настройка Stripe (для платежей)

1. Зарегистрируйтесь на https://stripe.com
2. Перейдите в Developer → API keys
3. Скопируйте `Publishable key` и `Secret key` (тестовые версии начинаются с `pk_test_` и `sk_test_`)
4. Добавьте их в `.env`:
   ```env
   STRIPE_PUBLIC_KEY=pk_test_ваш_ключ
   STRIPE_SECRET_KEY=sk_test_ваш_ключ
   ```

Тестовые карты для проверки:
- **Успешный платеж**: `4242 4242 4242 4242`
- **3D Secure**: `4000 0027 6000 3184`
- **Отклонение**: `4000 0000 0000 0002`
- CVV: любые 3 цифры
- Дата: любая будущая дата

### 5. Запуск

```bash
python manage.py runserver
```

Откройте http://localhost:8000

## Структура

```
online_shop/
├── backend/          # Django настройки
├── products/         # Товары, бренды
├── orders/           # Корзина, заказы
├── users/            # Пользователи
├── payments/         # Stripe
├── templates/        # HTML шаблоны
├── static/           # CSS, JS
└── manage.py
```

## Технологии

- Django 5.0.1 + DRF
- PostgreSQL
- Tailwind CSS + Alpine.js
- Celery + Redis
- Stripe

## Страницы

- `/` - Главная
- `/products/` - Каталог товаров
- `/brands/` - Список брендов
- `/cart/` - Корзина
- `/checkout/` - Оформление заказа (Stripe)
- `/wishlist/` - Избранное
- `/profile/` - Профиль пользователя
- `/admin/` - Админка Django
- `/api/docs/` - API документация (Swagger)

---

## Автор

worldpactleader © 2025
