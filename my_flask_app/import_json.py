# json는 소문자 열이고, import는 대문자로 해서 문제 발생.
import json
import sqlite3
import os

DB_PATH = "data/app.db"
JSON_PATH = "data/original.json"

def import_json():
    # === DB / JSON 경로 확인 ===
    print("DB_PATH (absolute):", os.path.abspath(DB_PATH))
    print("JSON_PATH (absolute):", os.path.abspath(JSON_PATH))

    # DB 연결
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # JSON 읽기
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # === DATA 구조 확인 ===
    print("type(data['DATA']):", type(data["DATA"]))
    rows = data["DATA"]

    # === 첫 row 구조 확인 ===
    print("첫 번째 row 전체 출력 ↓↓↓")
    print(rows[0])
    print("첫 번째 row keys ↓↓↓")
    print(rows[0].keys())

    batch = []

    for idx, row in enumerate(rows):

        # === 매핑 테스트 (딱 1번만) ===
        if idx == 0:
            print("매핑 테스트 ↓↓↓")
            print(
                row.get("cgg_nm"),        # 자치구명
                row.get("stdg_nm"),       # 법정동명
                row.get("bldg_nm"),       # 건물명
                row.get("bldg_usg"),      # 건물용도
                row.get("rent_area"),     # 임대면적
                row.get("grfe"),          # 보증금
                row.get("rtfe"),          # 임대료
                row.get("flr"),           # 층
                row.get("arch_yr"),       # 건축년도
                row.get("ctrt_day"),      # 계약일
            )

        batch.append((
            row.get("cgg_nm"),        # district
            row.get("stdg_nm"),       # dong
            row.get("bldg_nm"),       # building_name
            row.get("bldg_usg"),      # building_type
            float(row["rent_area"]) if row.get("rent_area") else None,
            int(row["grfe"]) if row.get("grfe") else None,
            int(row["rtfe"]) if row.get("rtfe") else None,
            int(row["flr"]) if row.get("flr") else None,
            int(row["arch_yr"]) if row.get("arch_yr") else None,
            row.get("ctrt_day")
        ))

        # === 1000개 단위 벌크 INSERT ===
        if len(batch) == 1000:
            cur.executemany("""
                INSERT INTO real_estate
                (district, dong, building_name, building_type,
                 area, deposit, rent, floor, built_year, contract_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, batch)
            batch = []

    # === 남은 데이터 INSERT ===
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
