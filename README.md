# Бот для создания алиасов в [mailcow](https://github.com/mailcow/mailcow-dockerized)

## О проекте

Telegram бот для удобного создания email-алиасов на почтовом сервере [mailcow](https://github.com/mailcow/mailcow-dockerized).

**Зачем?** При регистрации на сайтах можно использовать уникальные алиасы вида `site@my-domain.ru` вместо основного email. Бот избавляет от необходимости каждый раз заходить в панель управления mailcow для создания алиасов.

**Технологический стек:**
- 🐍 Python 3.13
- 🤖 [aiogram 3.x](https://docs.aiogram.dev/) — современная async библиотека для Telegram ботов
- 📦 SQLite — хранение списка авторизованных пользователей
- 🌐 HTTP прокси поддержка (PROXY_URL, PROXY_USERNAME, PROXY_PASSWORD)

## Быстрый старт

### Требования

- Python 3.13+
- Poetry для управления зависимостями

### Локальная разработка

```bash
# 1. Установить зависимости
poetry install

# 2. Создать .env из шаблона (для bash)
cp .env.example .env

# Или для Fish shell:
cp .env.fish.example .env.fish
source .env.fish

# 3. Запустить тесты
make test

# 4. Запустить бота
source .env && poetry run start
```

### Docker

```bash
# Запустить через docker run
docker run --name mailcow-aliases \
  --env-file .env \
  -v ${PWD}:/data \
  -d frog158/pymailcowaliasesbot

# Или через docker-compose
docker compose up -d
```

## Конфигурация

### Обязательные переменные окружения

```bash
# Telegram
TG_BOT_TOKEN="123456:ABCdef..."         # Токен бота от BotFather

# Mailcow
SERVER_URL="https://mail.example.com"   # URL mailcow сервера
X_API_KEY="your-api-key"                # API ключ из настроек mailcow
```

### Опциональные переменные

```bash
# Прокси (HTTP или SOCKS5)
PROXY_URL="192.168.1.100:3128"          # IP:PORT прокси сервера
PROXY_USERNAME="user"                   # Логин (если требуется)
PROXY_PASSWORD="pass"                   # Пароль (если требуется)

# База данных (обычно не менять)
DB_PATH="./data/user.db"                # Путь к SQLite БД (по умолчанию)
```

## Управление пользователями

Для работы бота нужно добавить авторизованных пользователей в БД.

### Добавить пользователя

```bash
# Локально
poetry run add_user 123456789 "Иван" "example.com" "ivan@example.com"

# В Docker
docker exec mailcow-aliases add_user 123456789 "Иван" "example.com" "ivan@example.com"
```

Параметры:
- `123456789` — Telegram ID пользователя
- `"Иван"` — Имя для логов
- `"example.com"` — Домен для создания алиасов
- `"ivan@example.com"` — Email для перенаправления почты

### Удалить пользователя

```bash
poetry run delete_user 123456789
docker exec mailcow-aliases delete_user 123456789
```

### Получить список пользователей

```bash
poetry run get_all_users
docker exec mailcow-aliases get_all_users
```

## Использование

1. Добавьте пользователя через CLI (см. выше)
2. Напишите боту в Telegram `/start` или `/help` для проверки доступа
3. Отправляйте названия алиасов текстом:
   - Отправляете: `gmail`
   - Бот создает: `gmail@example.com → ivan@example.com`
   - Ответ: `✅ Success! Address gmail@example.com goto ivan@example.com`

Если алиас не удалось создать (занят, ошибка), бот отправит сообщение об ошибке.

## Разработка

### Структура проекта

```
tg_mailcow_aliases/
  ├── bot.py          # Основная логика Telegram бота (aiogram)
  ├── api.py          # Интеграция с mailcow API
  ├── sqlite.py       # Работа с БД пользователей
  └── scripts/        # CLI команды
tests/
  └── test_sqlite.py  # Тесты (100% покрытие БД)
```

### Запуск тестов

```bash
make test
```

### Проверка кода

```bash
make lint
```

## История изменений

### v0.2.0 (2026-03-23)

- 🎉 Миграция с `telebot` на `aiogram 3.x`
  - Современная async/await архитектура
  - Лучшая производительность и надежность
- ✨ Добавлена поддержка HTTP/SOCKS5 прокси
  - Можно запустить бота из-за корпоративного прокси
- 📦 Python обновлен на 3.13
- 🧪 Все тесты проходят, 100% покрытие БД операций

### v0.1.1

- Исходная версия на pyTelegramBotAPI
- Базовая функциональность создания алиасов

## Лицензия

MIT 
