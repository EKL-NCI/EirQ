from flask import Flask, session, render_template, request,redirect, url_for
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import firebase_admin
from firebase_admin import credentials, db, auth ,firestore #Import from Firebase App
import pyrebase
from collections.abc import MutableMapping

app = Flask(__name__)
loggedInStatus = False

# Firebase service account cred!
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, options={'databaseURL': 'https://eirq-solutions-default-rtdb.europe-west1.firebasedatabase.app/'})

# Secret key for the app
app.config['SECRET_KEY'] = 'EirqSecretKey'

# PubNub configuration
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-6afc2464-b330-469f-a68d-52cbba8aecc4'
pnconfig.uuid = 'flask_demo_server'
pubnub = PubNub(pnconfig)
messages = []

# Firestore Client - Allow users to interact with firestore database
database = firestore.client()


# Firebase Confifuration
firebase_config = {   

            'apiKey': "AIzaSyCVDRhmU_ps8O0GNI9FjqmR6oh67ariS3s",
            'authDomain': "eirq-solutions.firebaseapp.com",
            'databaseURL': "https://eirq-solutions-default-rtdb.europe-west1.firebasedatabase.app",
            'projectId': "eirq-solutions",
            'storageBucket': "eirq-solutions.appspot.com",
            'messagingSenderId': "931290153741",
            'appId': "1:931290153741:web:d8edcb6428ff83a5352644",
            'measurementId': "G-KRKNJRRQMY"
}

firebase = pyrebase.initialize_app(firebase_config)  # Initialise Pyrebase with Firebase configuration
auth = firebase.auth()  # Get authentication object from Pyrebase)


class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        # Append received message to the messages list
        messages.append(message.message)
        # Stores the received message in Firebase Realtime Database
        ref = db.reference('air_quality')
        ref.push(message.message)
  

# Adding the listener and subscribing to the channel
def subscribe_to_channel():
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels('aq_channel').execute()


# Routing to pages
@app.route('/')
def index():
    return render_template('Index.html')  # This will render the HTML file with the PubNub subscription.

@app.route('/Login', methods=['GET', 'POST'])
def login():
    global loggedInStatus

    error_message = None

    if session.get('user'):
        loggedInStatus = True
        return redirect(url_for('dashboard'))   
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            loggedInStatus = True
            # Redirect to the sensors page upon successful login
            return redirect(url_for('dashboard'))
        except Exception as e:
            error_message = "Failed Login: {}".format(str(e))
            print("Login failed for user:", email, "with error:", str(e))  # Log failed login attempt

            # Check if the error message contains "INVALID_LOGIN_CREDENTIALS"
            if "INVALID_LOGIN_CREDENTIALS" in error_message:
                error_message = "Invalid email or password. Please try again."

            if "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
                error_message = "Too many failed login attempts. Please try again later or contact support."
    
    return render_template('Login.html' , error_message=error_message)


@app.route('/Signup', methods=['GET', 'POST'])
def signup():

    if session.get('user'):
        loggedInStatus = True
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        pwd0 = request.form['user_pwd0']
        pwd1 = request.form['user_pwd1']
        
        if pwd0 != pwd1:
            return render_template('Signup.html', error_message="Invalid Email or Passwords do not match")
        
        businessName = request.form['business-name']
        email = request.form['email']
        name = request.form['name']
        password = request.form['user_pwd1']

        # Check if the email already exists
        user_exists = check_email_exists(email)
        if user_exists:
            return render_template('Signup.html', error_message="Email already exists. Please login instead.")
        
        try:
            user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])

            users = {
                'name': name,
                'business-name': businessName,
                'email': email,
                'user_pwd1': password
            }  

            database.collection('User_data').add(users)  # Add user data to Firestore
            
            # Store the email in session to indicate that email verification is pending
            session['email_verification_pending'] = email

            # Redirect to the verify email page
            return render_template('Verify_email.html', email=email)

        except Exception as e:
            print("Error:", str(e))  # Print the error message for debugging
            return "Cannot be verified due to an error: {}".format(str(e))
        
    
    return render_template('Signup.html', message="SignUp successful!")

def check_email_exists(email):
    # Query Firestore to check if email already exists
    users_ref = database.collection('User_data')
    query = users_ref.where('email', '==', email).get()
    return len(query) > 0


@app.route('/Sensors')
def sensors():
    print("Data:", messages)
    return render_template('Sensors.html', data=messages)


@app.route('/Verify')
def verify_email():
    return render_template('Verify_email.html')


@app.route('/Chart')
def charts():
    return render_template('My_chart.html',data=messages)

@app.route('/Dashboard')
def dashboard():
    return render_template('Dashboard.html',data=messages)

@app.route('/Logout')
def logout():
    global loggedInStatus

    session.pop('user')
    loggedInStatus = False
    return redirect('/')

# Will catch any 404 error
if __name__ == '__main__':
    subscribe_to_channel()  # Start listening for PubNub messages
    app.run(debug=True)

