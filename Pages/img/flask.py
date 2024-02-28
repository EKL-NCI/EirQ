from flask import Flask, rendertemplate, urlfor
app = Flask(name)

@app.route('/')
def index():
    return rendertemplate('index.html')  # This will render the HTML file with the PubNub subscription.

if _name == '__main':
    app.run(debug=True)