from db import get_db
from datetime import datetime

def update_otp(code, public_id):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE user SET code = ? WHERE public_id = ?"
    cursor.execute(statement, [code, public_id])
    db.commit()
    return True

# Select User by Public ID
def validatePublicId (id): 
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM user WHERE public_id = ?" 
    cursor.execute(query, [id])
    return cursor.fetchone()

# Select User by Email. Search if the User exist.
def validate (email): 
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM user WHERE email = ?" 
    cursor.execute(query, [email])
    return cursor.fetchone()

# Select User & Password
def validatePassword (email, password): 
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM user WHERE email = ? AND password = ?" 
    cursor.execute(query, [email, password])
    return cursor.fetchone()

# Insert User
def insert (email, password, uuid): 
    db = get_db()
    cursor = db.cursor()
    query = "INSERT INTO user (email, password, public_id) VALUES (?, ?, ?)" 
    cursor.execute(query, [email, password, uuid])
    db.commit()
    return True