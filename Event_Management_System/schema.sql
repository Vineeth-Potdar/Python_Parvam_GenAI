CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    date TEXT NOT NULL,
    location TEXT NOT NULL,
    budget REAL NOT NULL,
    expected_guests INTEGER NOT NULL,
    ticket_price REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT NOT NULL,
    event_id INTEGER,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY (event_id) REFERENCES events (id)
);

CREATE TABLE IF NOT EXISTS vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    service_type TEXT NOT NULL,
    cost REAL NOT NULL,
    event_id INTEGER,
    FOREIGN KEY (event_id) REFERENCES events (id)
);