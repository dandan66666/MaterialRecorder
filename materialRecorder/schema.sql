DROP TABLE IF EXISTS material;

CREATE TABLE material (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    number INTEGER NOT NULL DEFAULT 1,
    record_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    specifications TEXT NOT NULL,
    price REAL NOT NULL
);