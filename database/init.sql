CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        email TEXT, 
        code TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
INSERT INTO user (email, code)
    VALUES( 'email@dominio.com', 000000 );
INSERT INTO user (email, code)
    VALUES( 'email1@dominio.com', 000000 );