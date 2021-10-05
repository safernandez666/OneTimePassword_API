from db import get_db


def update_otp(code, email):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE user SET code = ? WHERE email = ?"
    cursor.execute(statement, [code, email])
    db.commit()
    return True


# Select User by Email
def validate (email): 
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM user WHERE email = ?" 
    cursor.execute(query, [email])
    return cursor.fetchone()