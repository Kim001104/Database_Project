import json
import sqlite3

DB_PATH = "data/app.db"
JSON_PATH = "data/original.json"

def import_json():
    # DB 연결
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # JSON 읽기
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = data["DATA"]  # ★ 핵심: 우리가 사용할 실제 데이터!

    batch = []
    for row in rows:
        batch.append((
            row.get("자치구명"),
            row.get("법정동명"),
            row.get("건물명"),
            row.get("건물용도"),
            float(row["임대면적(㎡)"]) if row.get("임대면적(㎡)") else None,
            int(row["보증금(만원)"]) if row.get("보증금(만원)") else None,
            int(row["임대료(만원)"]) if row.get("임대료(만원)") else None,
            int(row["층"]) if row.get("층") else None,
            int(row["건축년도"]) if row.get("건축년도") else None,
            row.get("계약일")
        ))

        # 벌크 1000개씩 처리 (속도 매우 빠름)
        if len(batch) == 1000:
            cur.executemany("""
                INSERT INTO real_estate
                (district, dong, building_name, building_type,
                 area, deposit, rent, floor, built_year, contract_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, batch)
            batch = []

    # 남은 batch insert
    if batch:
        cur.executemany("""
            INSERT INTO real_estate
            (district, dong, building_name, building_type,
             area, deposit, rent, floor, built_year, contract_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, batch)

    conn.commit()
    conn.close()
    print("JSON → SQLite import 완료!")

if __name__ == "__main__":
    import_json()
