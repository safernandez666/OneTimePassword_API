from db import get_db
from datetime import datetime


def update_otp(code, email):
    db = get_db()
    cursor = db.cursor()
    # Convert to Data Object. Update the last Update to the Delta calculate
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
    statement = "UPDATE user SET code = ?, timestamp = ? WHERE email = ?"
    cursor.execute(statement, [code, time, email])
    db.commit()
    return True


# Select User by Email
def validate (email): 
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM user WHERE email = ?" 
    cursor.execute(query, [email])
    return cursor.fetchone()