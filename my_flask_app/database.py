import sqlite3
import os

# --- 디버그용 경로 출력 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DB_DIR, "app.db")

print("=== DEBUG ===")
print("BASE_DIR:", BASE_DIR)
print("DB_DIR:", DB_DIR)
print("DB_DIR exists?", os.path.isdir(DB_DIR))
print("DB_PATH:", DB_PATH)
print("================")

# data 폴더 없으면 자동 생성
os.makedirs(DB_DIR, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    sql_path = os.path.join(BASE_DIR, "models.sql")
    with open(sql_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
