import sqlite3

DB_PATH = "/opt/project/user.db"


def create_tabel():
    """Create database and user table if does not exists"""
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
    conn.close()


def add_user(id, name, domain, goto):
    """Add new user
    Args:
        id: telegram user ID
        name: name or nickname
        domain: in which domain will create aliases
        goto: email address for alias"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """INSERT INTO users
        (user_id, user_name, domain, goto)
        VALUES (?,?,?,?)""",
        (id, name, domain, goto),
    )
