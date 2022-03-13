import os, math, random, smtplib
# Import the email modules we'll need
from email.message import EmailMessage

######################################################################
#          Variables. Check .env for local propose                   #
######################################################################
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = 587
email_sender = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_PASSWORD')
######################################################################
#                            Functions                               #
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