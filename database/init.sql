CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        email TEXT, 
        password TEXT,
        code TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        public_id INTEGER
    );