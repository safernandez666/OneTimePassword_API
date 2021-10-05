from flask import Flask, jsonify, request
import user_controller
import os, math, random, smtplib
# Import the email modules we'll need
from email.message import EmailMessage

app = Flask(__name__) 

# Variables
smtp_server = os.getenv('STMP_SERVER')
smtp_port = 587
email_sender = os.getenv('EMAIL_SENDER')
email_password = os.getenv('EMAIL_PASSWORD')

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
    #s.sendmail(email,email_sender,msg)
    s.send_message(msg)
    s.quit()

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
    app.run(debug=True, host='0.0.0.0', port=5000)
