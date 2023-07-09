import pytest
import sqlite3
import os

from tg_mailcow_aliases.sqlite import add_user

DB_PATH = "/data/test_users.db"


@pytest.fixture(scope="module")
def setup_database():
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
    add_user("123", "Opa Opa", "opa.com", "opa@opa.com", DB_PATH)


def test_create_table(setup_database):
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
    add_user("234", "xlopa xlopa", "bubu.com", "bubu@bubu.com", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    result = c.fetchone()
    conn.close()
    assert result[0] == 1
