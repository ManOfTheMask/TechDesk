from flask import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login")
def child():
    return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)