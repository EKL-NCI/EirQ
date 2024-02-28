from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # This will render the HTML file with the PubNub subscription.

if __name__ == '__main__':
    app.run(debug=True)
