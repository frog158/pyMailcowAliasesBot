import sqlite3

DB_PATH = "/data/user.db"


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
        goto: email address for alias
        Return:
                None
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """INSERT INTO users
        (user_id, user_name, domain, goto)
        VALUES (?,?,?,?)""",
        (id, name, domain, goto),
    )
    conn.commit()
    conn.close()


def is_user_exist(id):
    """check if  user in database

    Args:
            id (strin): telegram user id
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE user_id=?", (id,))
    row = c.fetchone()
    conn.close()
    return row is not None


def get_user(id):
    """get user from database

    Args:
            id (string): telegram user id

    Returns:
            row: row or None
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT user_id, user_name, domain, goto FROM users WHERE user_id=?",
        (id,),
    )
    row = c.fetchone()
    conn.close()
    return row if row is not None else None


def delete_user(id):
    """delete user from database

    Args:
        id (string): user id from telegram
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "DELETE FROM users WHERE user_id=?",
        (id,),
    )
    conn.commit()
    conn.close()
