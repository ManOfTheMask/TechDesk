from flask import *
from flask_sqlalchemy import SQLAlchemy
import os, datetime, re

app = Flask(__name__)
key = os.environ.get("SECRET_KEY")
app.secret_key = str(key)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    role = db.Column(db.String(80))
    date_created = db.Column(db.String(80))


    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.date_created = datetime.datetime.now()
    
    def __repr__(self):
        return '<User %r>' % self.name

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    title = db.Column(db.String(100))
    description = db.Column(db.String(5000))
    status = db.Column(db.String(100))
    priority = db.Column(db.String(100))
    date_open = db.Column(db.String(100))
    date_close = db.Column(db.String(100))

    def __init__(self, author, title, description, status, priority, date_close):
        self.author = author
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.date_open = datetime.datetime.now()
        self.date_close = date_close

    def __repr__(self):
        return '<Ticket %r>' % self.title

@app.route('/')
def index():
    if session['username'] == None:
        session['username'] = "USERNAME"
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        found_username = Users.query.filter_by(username=username).first()
        found_password = Users.query.filter_by(password=password).first()
        if found_username:
            if found_password:
                session['username'] = username
                flash("you were successfully logged in")
                return redirect(url_for('dashboard'))
            else:
                flash("incorrect password")
                return redirect(url_for('login'))
        else:
            flash("you were not found in the database please sign up")
            return redirect(url_for('signup'))
            

    else:
        if "username" in session:
            return redirect(url_for("dashboard"))
        else:
            return render_template('login.html')

@app.route("/signup" , methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        #check username for weblink friendly characters only
        if re.match("[^A-Za-z0-9]+", username):
            
            flash("username must be alphanumeric")
            return redirect(url_for('signup'))
        else:
            found_username = Users.query.filter_by(username=username).first()
            if found_username:
                flash("username already exists")
                return redirect(url_for('login'))
            else:
                session['username'] = username
                new_user = Users(username, email, password, role)
                db.session.add(new_user)
                db.session.commit()
                flash(f"you were successfully signed up {new_user.username}" )
                if role == "technician":
                   return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('ticketsubmission'))
        
    else:
        return render_template('signup.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    tickets = Tickets.query.all()
    return render_template("dashboard.html", tickets=tickets)

@app.route("/ticketsubmission", methods=['GET', 'POST'])
def ticketsubmission():
    if request.method == "POST":
        ticketAuthor = session['username']
        ticketTitle = request.form['ticketTitle']
        ticketDescription = request.form['ticketDescription']
        ticketPriority = request.form['ticketPriority']

        new_ticket = Tickets(ticketAuthor, ticketTitle, ticketDescription, ticketPriority, "open","none")
        db.session.add(new_ticket)
        db.session.commit()
        flash("ticket submitted")
        return redirect(url_for('dashboard'))
    else:
        if "username" in session:
            return render_template('ticketsubmission.html')
        else:
            flash("you must be logged in to submit a ticket")
            return redirect(url_for('login'))

@app.route("/profiles/<string:username>")
def profiles(username):
    user = Users.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)

@app.route("/tickets/<int:id>")
def ticket(id):
    ticket = Tickets.query.get_or_404(id)
    return render_template("ticketdetails.html", ticket=ticket)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)