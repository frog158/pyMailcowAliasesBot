import sqlite3

DB_PATH = "/data/user.db"


def create_tabel(db=DB_PATH):
    """Create database and user table if does not exists"""
    connection = sqlite3.connect(db)
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
    connection.close()


def add_user(id, name, domain, goto, db=DB_PATH):
    """Add new user
    Args:
        id: telegram user ID
        name: name or nickname
        domain: in which domain will create aliases
        goto: email address for alias
        Return:
                None
    """
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO users
        (user_id, user_name, domain, goto)
        VALUES (?,?,?,?)""",
        (id, name, domain, goto),
    )
    connection.commit()
    connection.close()


def is_user_exist(id, db=DB_PATH):
    """check if  user in database

    Args:
            id (strin): telegram user id
    """
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (id,))
    row = cursor.fetchone()
    connection.close()
    return row is not None


def get_user(id, db=DB_PATH):
    """get user from database

    Args:
            id (string): telegram user id

    Returns:
            row: row or None
    """
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT user_id, user_name, domain, goto FROM users WHERE user_id=?",
        (id,),
    )
    row = cursor.fetchone()
    connection.close()
    return row if row is not None else None


def delete_user(id, db=DB_PATH):
    """delete user from database

    Args:
        id (string): user id from telegram
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(
        "DELETE FROM users WHERE user_id=?",
        (id,),
    )
    conn.commit()
    conn.close()


def get_all_users(db=DB_PATH):
    """get all users from database

    Returns:
        list: return list of tuples of all users
    """
    sql = "SELECT * FROM users"
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(sql)
    result = c.fetchall()
    conn.close()
    return result
