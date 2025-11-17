import sqlite3

DB_PATH = "/data/app.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # dict처럼 사용 가능
    return conn

def init_db():
    conn = get_db()
    with open("models.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
