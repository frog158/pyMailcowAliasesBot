# Контекст проекта для Claude

## 📖 Документация проекта

- [📊 Анализ проекта](docs/ANALYSIS.md) - полный разбор архитектуры, компонентов, проблем и рекомендаций
- [📚 README](README.md) - описание установки и использования бота

## 🎯 О проекте

**pyMailcowAliasesBot** - Telegram-бот для создания email-алиасов в mailcow почтовом сервере.

**Основные компоненты**:
- `bot.py` - основная логика Telegram-бота
- `api.py` - интеграция с API mailcow
- `sqlite.py` - управление пользователями в БД
- `tests/` - тесты для БД операций (100% покрытие)

**Стек**: Python 3.11+, telebot, requests, sqlite3

## 🚀 Быстрый старт

```bash
# Установка зависимостей
poetry install

# Создание таблицы БД
poetry run create_table

# Добавление пользователя
poetry run add_user 123456 "John" "example.com" "john@example.com"

# Запуск бота
poetry run start
```

## ⚠️ Приоритетные проблемы

1. **Error handling** для сетевых ошибок (api.py)
2. **Валидация входных данных** (email, alias формат)
3. **Type hints** для всех функций
4. **Опечатка**: `create_tabel()` → `create_table()`

Подробнее см. в [docs/ANALYSIS.md](docs/ANALYSIS.md#-проблемы-и-замечания)

## 📝 Заметки для работы

- Все операции с БД уже имеют тесты
- SQL запросы защищены от injection (параметризованные)
- Проект использует Poetry для управления зависимостями
- Поддерживается Docker для развертывания

---

Для полного анализа проекта см. [docs/ANALYSIS.md](docs/ANALYSIS.md)
