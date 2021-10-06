from flask import Flask, jsonify, request, abort
import user_controller
import os, math, random, smtplib
from datetime import datetime
# Import the email modules we'll need
from email.message import EmailMessage
from functools import wraps

app = Flask(__name__) 

# Variables
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = 587
email_sender = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_PASSWORD')
timeToLease = 5 # Time to change the OTP. It's in Minutes.
app.config['API_KEY'] = os.getenv('API_KEY', None)

######################################################################
# HTTP Error Handlers
######################################################################
@app.errorhandler(401)
def not_authorized(e):
    """ Respose sent back when not autorized """
    return jsonify(status=401, error='Not Authorized',
                   message='You are authorized to access the URL requested.'), 401

######################################################################
# Check Auth: Add your autorization code here
######################################################################
def check_auth():
    """ Checks the environment that the API_KEY has been set """
    if app.config['API_KEY']:
        return app.config['API_KEY'] == request.headers.get('X-Api-Key')
    return False

######################################################################
# Requires API Key: Decorator function to add secuity to any call
######################################################################
def requires_apikey(f):
    """ Decorator function to require API Key """
    @wraps(f)
    def decorated(*args, **kwargs):
        """ Decorator function that does the checking """
        if check_auth():
            return f(*args, **kwargs)
        else:
            abort(401)
    return decorated
######################################################################
# Functions
######################################################################   

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
    msg['From'] = "OTP Message <%s>" % email_sender
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

# Validate Email
def validateEmail(email):
    result = user_controller.validate(email)
    if result:
        return True
    else:
        return False
######################################################################
# Routes & Services
######################################################################  
# Iniciate Process
@app.route("/v1/init", methods=["GET"])
@requires_apikey
def update_otp():
    user_details = request.get_json()
    email = user_details["email"]
    status = validateEmail(email)
    if status:
        code = generateOneTimePassword()
        result = user_controller.update_otp(code, email)
        sendEmail(email, code)
        return jsonify({'message': 'The code was generated'}), 200
    else:
        return jsonify({'message': 'This email dont exist'}), 404        

# Validete email & Code
@app.route("/v1/validate", methods=["POST"])
@requires_apikey
def validate(): 
    user_details = request.get_json()
    email = user_details["email"]
    code = user_details["code"]
    result = user_controller.validate(email)
    # Validate Code and email within delta.
    if result:
        if ((result[1] == email) and (result[2] == str(code)) and (delta(result[3],timeToLease) == True)):
            return jsonify({'message': 'The code is valid'}), 200
        else:
            return jsonify({'message': 'Bad Request'}), 404        
    return jsonify({'message': 'This email dont exist'}), 404
######################################################################
# Main Program
######################################################################  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
