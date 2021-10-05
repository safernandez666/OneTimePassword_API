from flask import Flask, jsonify, request
import user_controller
import os, math, random, smtplib

app = Flask(__name__) 

# Variables
smtp_server = "smtp.hostinger.com.ar"
smtp_port = 587
email_sender = "xxx@ironbox.com.ar"
email_password = "xxx"

# Generate One Time Password
def generateOneTimePassword():
    digits="0123456789"
    OTP=""
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    return OTP

# Send Email
def sendEmail(email, code):
    s = smtplib.SMTP(smtp_server, smtp_port)
    s.starttls()
    s.login(email_sender, email_password)
    s.sendmail(email,email_sender,code)

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
    # Validate Code and email
    if result:
        if (result[2] == str(code)):
            return jsonify({'message': 'The code is valid'}), 200
        else:
            return jsonify({'message': 'The code is invalid'}), 404        
    return jsonify({'message': 'This email dont exist'}), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
