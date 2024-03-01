from flask import Flask, render_template, url_for, request, redirect
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

# Firebase info will go here !

app = Flask(__name__)

# PubNub configuration
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-6afc2464-b330-469f-a68d-52cbba8aecc4'
pnconfig.uuid = 'flask_demo_server'
pubnub = PubNub(pnconfig)
messages = []

class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, message):
        messages.append(message.message)

# Adding the listener and subscribing to the channel
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('aq_channel').execute()

print("Messages: ", messages)

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

if __name__ == '__main__':
    app.run(debug=True)
