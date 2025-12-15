from flask import Flask, render_template, jsonify, request
from database import get_db, init_db

app = Flask(__name__)

with app.app_context():
    init_db()

@app.route("/")
def home():
    return render_template("index.html")

# ✅ (기존) 자치구별 평균 월세
@app.route("/api/avg-rent")
def avg_rent():
    db = get_db()
    rows = db.execute("""
        SELECT district, AVG(rent) AS avg_rent
        FROM real_estate
        WHERE rent IS NOT NULL
        GROUP BY district
        ORDER BY avg_rent DESC
    """).fetchall()

    return jsonify({
        "labels": [r["district"] for r in rows],
        "values": [round(r["avg_rent"], 1) for r in rows]
    })

# ✅ (신규) Step 확장 페이지
@app.route("/drilldown")
def drilldown():
    return render_template("drilldown.html")

# ✅ (신규) 자치구 목록 API
@app.route("/api/districts")
def districts():
    db = get_db()
    rows = db.execute("""
        SELECT DISTINCT district
        FROM real_estate
        WHERE district IS NOT NULL
        ORDER BY district
    """).fetchall()

    return jsonify([r["district"] for r in rows])

# ✅ (신규) 특정 자치구의 동 목록 API
@app.route("/api/dongs")
def dongs():
    district = request.args.get("district")
    if not district:
        return jsonify([])

    db = get_db()
    rows = db.execute("""
        SELECT DISTINCT dong
        FROM real_estate
        WHERE district = ?
          AND dong IS NOT NULL
        ORDER BY dong
    """, (district,)).fetchall()

    return jsonify([r["dong"] for r in rows])

@app.route("/api/stats/avg")
def avg_stats():
    district = request.args.get("district")
    dong = request.args.get("dong")
    building_type = request.args.get("building_type")

    min_area = request.args.get("min_area")  # ㎡
    max_area = request.args.get("max_area")  # ㎡

    if not district or not dong or not building_type:
        return jsonify({})

    query = """
        SELECT
            AVG(rent) AS avg_rent,
            AVG(deposit) AS avg_deposit,
            COUNT(*) AS total_count
        FROM real_estate
        WHERE district = ?
          AND dong = ?
          AND building_type = ?
    """
    params = [district, dong, building_type]

    if min_area:
        query += " AND area >= ?"
        params.append(float(min_area))

    if max_area:
        query += " AND area <= ?"
        params.append(float(max_area))

    db = get_db()
    row = db.execute(query, params).fetchone()

    return jsonify({
        "avg_rent": round(row["avg_rent"], 1) if row["avg_rent"] else None,
        "avg_deposit": round(row["avg_deposit"], 1) if row["avg_deposit"] else None,
        "total_count": row["total_count"]
    })


# 건물 유형별 비율 API 
@app.route("/api/stats/building-type")
def building_type_stats():
    district = request.args.get("district")
    dong = request.args.get("dong")

    if not district or not dong:
        return jsonify([])

    db = get_db()
    rows = db.execute("""
        SELECT
            building_type,
            COUNT(*) AS cnt
        FROM real_estate
        WHERE district = ?
          AND dong = ?
          AND building_type IS NOT NULL
        GROUP BY building_type
        ORDER BY cnt DESC
    """, (district, dong)).fetchall()

    return jsonify({
        "labels": [r["building_type"] for r in rows],
        "values": [r["cnt"] for r in rows]
    })

# 자치구, 동, 건물 유형에 대한 조회 데이터
@app.route("/api/contracts")
def contracts():
    district = request.args.get("district")
    dong = request.args.get("dong")
    building_type = request.args.get("building_type")

    min_area = request.args.get("min_area")  # ㎡
    max_area = request.args.get("max_area")  # ㎡

    if not district or not dong or not building_type:
        return jsonify([])

    query = """
        SELECT
            area,
            rent,
            deposit,
            contract_date
        FROM real_estate
        WHERE district = ?
          AND dong = ?
          AND building_type = ?
    """
    params = [district, dong, building_type]

    if min_area:
        query += " AND area >= ?"
        params.append(float(min_area))

    if max_area:
        query += " AND area <= ?"
        params.append(float(max_area))

    query += " ORDER BY rent ASC LIMIT 500"

    db = get_db()
    rows = db.execute(query, params).fetchall()

    return jsonify([
        {
            "area": r["area"],
            "rent": r["rent"],
            "deposit": r["deposit"],
            "contract_date": r["contract_date"]
        }
        for r in rows
    ])





if __name__ == "__main__":
    app.run(debug=True)
