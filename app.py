from flask import Flask, jsonify, request, abort, make_response
import jwt
import user_controller, functions
import os, jwt, uuid, datetime
from datetime import date, datetime, time, timedelta
from functools import wraps

app = Flask(__name__) 

######################################################################
# Variables. Check .env for local propose
######################################################################
app.config['API_KEY'] = os.getenv('API_KEY', None)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', None)

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
#   Requires API Key: Decorator function to add secuity to any call  #
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
#   Requires Token: Decorator function to add secuity to any call    #
######################################################################
def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None

      if 'x-access-tokens' in request.headers:
         token = request.headers['x-access-tokens']

      if not token:
         return jsonify({'message': 'a valid token is missing'})

      try:
         data=jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256', ])
         current_user = user_controller.validatePublicId(data['public_id'])
      except:
         return jsonify({'message': 'token is invalid'})

      return f(current_user, *args, **kwargs)
   return decorator

######################################################################
#                     Validate the Parameters                        #
######################################################################
def required_params(required):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _json = request.get_json()
            missing = [r for r in required.keys()
                       if r not in _json]
            if missing:
                response = {
                    "status": "error",
                    "message": "Request JSON is missing some required params",
                    "missing": missing
                }
                return jsonify(response), 400
            wrong_types = [r for r in required.keys()
                           if not isinstance(_json[r], required[r])]
            if wrong_types:
                response = {
                    "status": "error",
                    "message": "Data types in the request JSON doesn't match the required format",
                    "param_types": {k: str(v) for k, v in required.items()}
                }
                return jsonify(response), 400
            return fn(*args, **kwargs)
        return wrapper
    return decorator

######################################################################
# Routes & Services
######################################################################  

# Singup
@app.route('/v1/singup', methods =['POST'])
@requires_apikey
@required_params({"email": str, "password": str})
def signup():
    user_details = request.get_json()
    email, password = user_details["email"], user_details["password"]
    # checking for existing user
    user = user_controller.validate(email)
    if not user:
        if user_controller.insert(email, password, str(uuid.uuid4())):
            return jsonify({'message': 'Succesfull Register'}), 200
        else:  
            return jsonify({'message': 'Error on the Insert'}), 401 
    else:
        # returns 202 if user already exists
        return jsonify({'message': 'This User Exist, please Login'}), 202   

# Login
@app.route('/v1/login', methods =['POST'])
@requires_apikey
@required_params({"email": str, "password": str})
def login():
    user_details = request.get_json()
    email, password = user_details["email"], user_details["password"]   
    # checking for existing user and the Password
    result = user_controller.validatePassword(email, password)
    if not result:
        # returns 401 if any email or / and password is missing
        return jsonify({'message': 'Could not Verify'}), 401  
    # Check User & Password from DDBB vs Paramaters
    if result:
        # generates the JWT Token
        token = jwt.encode({'public_id': result[5], 'exp' : datetime.combine(date.today(), time(23, 55)) + timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')  
        return jsonify({'token' : token}) 
    else:  
        # returns 401 if any email or / and password is missing
        return jsonify({'message': 'Could not Verify'}), 401     

# Iniciate Process with Token
@app.route("/v1/init", methods=["GET"])
@required_params({"email": str, "password": str})
@token_required
def update_otp(current_user):
    user_details = request.get_json()
    email, password = user_details["email"], user_details["password"]   
    # checking for existing user and the Password
    result = user_controller.validatePassword(email, password)
    if not result:
        # returns 401 if any email or / and password is missing
        return jsonify({'message': 'Could not Verify'}), 401 
    # Generate OTP
    if current_user[5] == result[5]:
        code = functions.generateOneTimePassword()
        user_controller.update_otp(code, current_user[5])
        functions.sendEmail(current_user[1], code)
        return jsonify({'message': 'The code was generated'}), 200
    else:
        return jsonify({'message': 'Something its wrong.'}), 404   

# Validete email & Code with Token
@app.route("/v1/validate", methods=["POST"])
@token_required
@required_params({"email": str, "password": str, "code": int})
def validate(current_user): 
    user_details = request.get_json()
    email, password = user_details["email"], user_details["password"]   
    # checking for existing user and the Password
    result = user_controller.validatePassword(email, password)
    # Validate Code and Public_Id within delta.
    if result:
        if (current_user[5] == result[5] and result[3] == str(user_details["code"])):
            return jsonify({'message': 'The code is valid'}), 200
        else:
            return jsonify({'message': 'Bad Request'}), 404                
    return jsonify({'message': 'This email dont exist'}), 404

######################################################################
# Main Program
######################################################################  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
