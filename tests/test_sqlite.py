import pytest
import sqlite3
import os

from tg_mailcow_aliases.sqlite import add_user

DB_PATH = "/data/test_users.db"


@pytest.fixture(scope="module")
def setup_database():
    """
    Фикстура для настройки базы данный перед выполнением модульных тестов.
    Предусловия: Нет.
    Ожидаемые результаты: База данных будет создана и подготовлена для
    выполнения тестов
    """
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        user_name TEXT,
        domain TEXT,
        goto TEXT)"""
    )
    conn.commit()
    yield
    conn.close()
    os.remove(DB_PATH)


@pytest.fixture()
def setup_test_data(setup_database):
    """
    Фикстура для добавления тестовых данных в базу данных
    Предусловия: Подготовленная и настроенная база данных
    Ожидаемые результаты: Тестовые данные будут успешно добавлены
    в таблицу `users`
    """
    add_user("123", "Opa Opa", "opa.com", "opa@opa.com", DB_PATH)


def test_create_table(setup_database):
    """
    Проверяет создание таблицы `users` в базе данных
    Предусловия: База данных пуста или отсутствует
    Ожидаемые результаты: Таблица `users` должна быть успешно создана
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """SELECT name FROM sqlite_master
        WHERE type='table' and name='users'"""
    )
    result = c.fetchone()
    conn.close()
    assert result[0] == "users"


def test_add_user(setup_database):
    """
    Проверяет добавление пользователя в базу данных
    Предусловия: База данных пуста
    Ожидаемые резулльтаты: Пользователь должен быть успешно добавлен
    в таблицу `users`
    """
    add_user("234", "xlopa xlopa", "bubu.com", "bubu@bubu.com", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    result = c.fetchone()
    conn.close()
    assert result[0] == 1
