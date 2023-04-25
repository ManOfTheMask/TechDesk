from flask import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/child")
def child():
    return render_template('child.html')
if __name__ == '__main__':
    app.run(debug=True)