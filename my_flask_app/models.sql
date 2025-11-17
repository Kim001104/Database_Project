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
);