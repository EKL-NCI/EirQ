from flask import Flask, render_template, url_for, request, redirect, flash
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import firebase_admin
from firebase_admin import credentials, db
from flask_mysqldb import MySQL  
import bcrypt

# Firebase info will go here !
cred = credentials.Certificate("EirQ/credentials.json")
try:
    firebase_admin.initialize_app(cred, name="sensors", options={'databaseURL': 'https://eirq-solutions-default-rtdb.europe-west1.firebasedatabase.app/'})
except ValueError as e:
    print("Error initializing Firebase:", e)
# Secret key for the app
app.config['SECRET_KEY'] = 'EirqSecretKey'

# PubNub configuration
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-6afc2464-b330-469f-a68d-52cbba8aecc4'
pnconfig.uuid = 'flask_demo_server'
pubnub = PubNub(pnconfig)
messages = []

#MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQ:L_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'eirq'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

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

@app.route('/Sensors')
def sensors():
    return render_template('sensors.html', data=messages)

@app.route('/Login', methods=['GET', 'POST'])
def Login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form.get('password').encode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', [email])
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid login credentials. Please try again.', 'error')
            pass

    return render_template('Login.html')

@app.route('/Signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        business_name = request.form.get('business-name')
        email = request.form.get('email')
        password = request.form.get('password').encode('utf-8')

        # Hashing the password
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (business_name, email, hashed_password.decode('utf-8')))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('Login'))

    return render_template('Signup.html')

# Will catch any 404 error
if __name__ == '__main__':
    app.run(debug=True)
