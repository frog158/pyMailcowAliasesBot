import pytest
import sqlite3
import os

from tg_mailcow_aliases.sqlite import (
    add_user,
    is_user_exist,
    get_user,
    delete_user,
    get_all_users,
)

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
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        user_name TEXT,
        domain TEXT,
        goto TEXT)"""
    )
    connection.commit()
    yield
    connection.close()
    os.remove(DB_PATH)


@pytest.fixture()
def setup_test_data(setup_database):
    """
    Фикстура для добавления тестовых данных в базу данных
    Предусловия: Подготовленная и настроенная база данных
    Ожидаемые результаты: Тестовые данные будут успешно добавлены
    в таблицу `users`
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO users
        (user_id, user_name, domain, goto)
        VALUES (?,?,?,?)""",
        ("123", "Opa Opa", "opa.com", "opa@opa.com"),
    )
    connection.commit()
    connection.close()


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
    assert result == ("users",)


def test_add_user(setup_database):
    """
    Проверяет добавление пользователя в базу данных
    Предусловия: База данных пуста
    Ожидаемые результаты: Пользователь должен быть успешно добавлен
    в таблицу `users`
    """
    add_user("234", "xlopa xlopa", "bubu.com", "bubu@bubu.com", DB_PATH)
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    result = cursor.fetchone()
    connection.close()
    assert result == (1,)


def test_is_user_exists(setup_test_data):
    """
    Проверяет есть ли пользователь в таблице
    Предусловия: База данных создана, добавлены тестовые данные
    Ожидаемые результаты: True если пользователь есть
    False если пользователя нет
    """
    # True
    assert is_user_exist("234", DB_PATH)
    # True
    assert is_user_exist("123", DB_PATH)
    # False
    assert not is_user_exist("128", DB_PATH)


def test_get_user(setup_test_data):
    """
    Получает данные пользователя из базы
    Предусловия: База данных создана, добавлены тестовые данные
    Ождаемые результаты:
    ("123", "Opa Opa", "opa.com", "opa@opa.com")
    None
    """
    user = get_user("123", DB_PATH)
    assert user == ("123", "Opa Opa", "opa.com", "opa@opa.com")
    user = get_user("112233", DB_PATH)
    assert user is None


def test_delete_user(setup_test_data):
    """
    Удаляет пользователя из базы данных
    Предусловия: База данных создана, добавлены тестовые данные
    Ожидаемые результаты: Пользователь удален из базы данных
    """
    assert is_user_exist("123", DB_PATH)
    delete_user("123", DB_PATH)
    assert not is_user_exist("123", DB_PATH)
    assert is_user_exist("234", DB_PATH)
    delete_user("234", DB_PATH)
    assert not is_user_exist("234", DB_PATH)


def test_get_all_users(setup_test_data):
    """
    Получает всех пользователей из базы данных
    Предусловия: База данных создана, добавлены тестовые данные
    Ожидаемые результаты: Список пользователей
    """
    assert get_all_users(DB_PATH) == [
        (5, "123", "Opa Opa", "opa.com", "opa@opa.com")
    ]
