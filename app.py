from flask import Flask, jsonify, request
import user_controller
import os, math, random, smtplib
from datetime import datetime
# Import the email modules we'll need
from email.message import EmailMessage

app = Flask(__name__) 

# Variables
smtp_server = 'smtp.xx.com.ar'
smtp_port = 587
email_sender = 'XX'
email_password = 'XX'
timeToLease = 1 # Time to change the OTP. It's in Minutes.

# Generate One Time Password
def generateOneTimePassword():
    digits="0123456789"
    OTP=""
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    return OTP

# Send Email
def sendEmail(email, code):
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content("Your One Time Passoword is: " + code)
    msg['Subject'] = f'One Time Password'
    msg['From'] = "OTP Message <%s>" % email
    msg['To'] = email
    s = smtplib.SMTP(smtp_server, smtp_port)
    s.starttls()
    s.login(email_sender, email_password)
    s.send_message(msg)
    s.quit()

# Delta
def delta(time, timeToLease):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Convert to Data Object
    d1 = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    time_delta = (d1 - d2)
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds/60
    if minutes <= timeToLease:
        return True
    else:
        return False

# Iniciate Process
@app.route("/v1/init", methods=["GET"])
def update_otp():
    user_details = request.get_json()
    email = user_details["email"]
    code = generateOneTimePassword()
    result = user_controller.update_otp(code, email)
    if result:
        sendEmail(email, code)
        return jsonify({'message': 'The code was generated'}), 200
    else:
        return jsonify({'message': 'This email dont exist'}), 404        

# Validete email & Code
@app.route("/v1/validate", methods=["POST"])
def validate():
    user_details = request.get_json()
    email = user_details["email"]
    code = user_details["code"]
    result = user_controller.validate(email)
    # Validate Code and email within delta.
    if result:
        if ((result[2] == str(code)) and (delta(result[3],timeToLease) == True)):
            return jsonify({'message': 'The code is valid'}), 200
        else:
            return jsonify({'message': 'Bad Request'}), 404        
    return jsonify({'message': 'This email dont exist'}), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
