from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "1232321"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    role = db.Column(db.String(80))


    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
    
    def __repr__(self):
        return '<User %r>' % self.name

class ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.Text)
    priority = db.Column(db.Text)
    date_open = db.Column(db.Text)
    date_close = db.Column(db.Text)

    def __init__(self, author, title, description, status, priority, date_open, date_close):
        self.author = author
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.date_open = date_open
        self.date_close = date_close

    def __repr__(self):
        return '<Ticket %r>' % self.title

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/logout")
def logout():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/ticketsubmission")
def ticketsubmission():
    return render_template('ticketsubmission.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route("/ticket")
def ticket():
    return render_template("ticketdetails.html")

if __name__ == '__main__':
    # investigate why it needs to run with app context
    with app.app_context():
        db.create_all()
        #test commands
        #new_user = user("admin", "admin@gmail.com", "admin", "techition")
        #db.session.add(new_user)
        #db.session.commit()
    app.run(debug=True)