from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import firebase_admin
from firebase_admin import credentials, db

# Firebase info will go here !
cred = credentials.Certificate("credentials.json")
try:
    firebase_admin.initialize_app(cred, name="sensors", options={'databaseURL': 'https://eirq-solutions-default-rtdb.europe-west1.firebasedatabase.app/'})
except ValueError as e:
    print("Error initializing Firebase:", e)

# App instance
app = Flask(__name__)


# Connects app file to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Secret key for the app
app.config['SECRET_KEY'] = 'admin'
# User Database Innstance
db_users = SQLAlchemy(app)

class User(db_users.Model, UserMixin):
    id = db_users.Column(db_users.Integer, primary_key=True)
    username = db_users.Column(db_users.String(20), unique=True, nullable=False)
    password = db_users.Column(db_users.String(80), nullable=False)


# PubNub configuration
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-6afc2464-b330-469f-a68d-52cbba8aecc4'
pnconfig.uuid = 'flask_demo_server'
pubnub = PubNub(pnconfig)
messages = []

class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        # Append received message to the messages list
        messages.append(message.message)
        # Stores the received message in Firebase Realtime Database
        ref = db.reference('/air_quality')
        ref.push(message.message)

# Adding the listener and subscribing to the channel
def subscribe_to_channel():
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels('aq_channel').execute()

# Routing to pages

@app.route('/')
def index():
    return render_template('Index.html')  # This will render the HTML file with the PubNub subscription.

@app.route('/Login')
def Login():
    return render_template('Login.html')

@app.route('/Sensors')
def sensors():
    return render_template('sensors.html', data=messages)

@app.route('/Signup')
def sign_up():
    return render_template('Signup.html')

# Will catch any 404 error
if __name__ == '__main__':
    app.run(debug=True)
