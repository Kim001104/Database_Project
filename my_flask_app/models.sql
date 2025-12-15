-- original.json 파일에서 필요한 요소만 추출하여 테이블 만들기
CREATE TABLE IF NOT EXISTS real_estate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    district TEXT,
    dong TEXT,
    building_name TEXT,
    building_type TEXT,
    area REAL,
    deposit INTEGER,
    rent INTEGER,
    floor INTEGER,
    built_year INTEGER,
    contract_date TEXT

    CHECK (area IS NULL OR area > 0),   --무결성 제약 조건
    CHECK (rent IS NULL OR rent >= 0),  --무결성 제약 조건  
    CHECK (deposit IS NULL OR deposit >= 0) --무결성 제약 조건
);