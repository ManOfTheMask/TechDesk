from flask import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/ticketsubmission")
def ticketsubmission():
    return render_template('ticketsubmission.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)