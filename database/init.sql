CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        email INTEGER, 
        code TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
INSERT INTO user (email, code)
    VALUES( 'sfernandez@ironbox.com.ar', 000000 );
INSERT INTO user (email, code)
    VALUES( 'vanesacurto@gmail.com', 000000 );