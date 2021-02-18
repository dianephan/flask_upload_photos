import os
from dotenv import load_dotenv
from twilio.rest import Client
from flask import Flask, request, render_template, redirect, session, url_for
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

load_dotenv()
app = Flask(__name__)
app.secret_key = 'dsfdsd'
app.config.from_object('settings')

UPLOAD_FOLDER = 'UPLOADS'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png']

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= os.environ.get('TWILIO_AUTH_TOKEN')
VERIFY_SERVICE_SID= os.environ.get('VERIFY_SERVICE_SID')
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

KNOWN_PARTICIPANTS = app.config['KNOWN_PARTICIPANTS']

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']
   # returns T/F if '.' in filename and the extension is parsed correctly 

@app.route('/', methods=['GET', 'POST'])
def login():
   error = None
   if request.method == 'POST':
      username = request.form['username']
      if username in KNOWN_PARTICIPANTS:
         session['username'] = username
         send_verification(username)
         return redirect(url_for('generate_verification_code'))
      error = "User not found. Please try again."
      return render_template('index.html', error = error)
   return render_template('index.html')

def send_verification(username):
   phone = KNOWN_PARTICIPANTS.get(username)
   client.verify \
      .services(VERIFY_SERVICE_SID) \
      .verifications \
      .create(to=phone, channel='sms')

@app.route('/verifyme', methods=['GET', 'POST'])
def generate_verification_code():
   username = session['username']
   phone = KNOWN_PARTICIPANTS.get(username)
   error = None
   if request.method == 'POST':
      verification_code = request.form['verificationcode']
      if check_verification_token(phone, verification_code):
         # return render_template('uploadpage.html', username = username)
         return redirect(url_for('upload_file'))
      else:
         error = "Invalid verification code. Please try again."
         return render_template('verifypage.html', error = error)
   return render_template('verifypage.html', username = username)

def check_verification_token(phone, token):
   check = client.verify \
      .services(VERIFY_SERVICE_SID) \
      .verification_checks \
      .create(to=phone, code=token)    
   return check.status == 'approved'

@app.route('/upload')
def upload_file():
   return render_template('uploadpage.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def submitted_file():
   username = session['username']
   if request.method == 'POST':
      f = request.files['file']
      if f and allowed_file(f.filename):
         f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
         return render_template('success.html',  username = username)
      # print("[INFO] : f = ", f)
      # [INFO] : f =  <FileStorage: 'Screen Shot 2021-01-31 at 10.18.40 PM.png' ('image/png')>
      # if f.filename == '':
      else:
         error = "Please upload a valid file."
         return render_template('uploadpage.html', username = username, error = error)
