import sqlite3

DB_PATH = "/opt/project/user.db"


def create_tabel():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users
     (id INTEGER PRIMARY KEY AUTOINCREMENT,
     user_id TEXT,
     user_name TEXT,
     domain TEXT,
     goto TEXT) """
    )
    conn.commit()
    conn.close()
    pass
