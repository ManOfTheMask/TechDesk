from flask import *
from flask_sqlalchemy import SQLAlchemy
import os, datetime, re

#app configuration
app = Flask(__name__)
key = os.environ.get("SECRET_KEY")
app.secret_key = str(key)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

#Database model classes
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
    # if username session keyvalue is not in session
    if 'username' not in session:
        #make a guest keyvalue pair
        session['username'] = "USERNAME"
    #send the user to the login screen
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    #if user submits login 
    if request.method == "POST":
        #grab data from form
        username = request.form['username']
        password = request.form['password']
        #search database for data from form
        found_username = Users.query.filter_by(username=username).first()
        found_password = Users.query.filter_by(password=password).first()
        #if username matches
        if found_username:
            #check if password matches username
            if found_password:
                #set session username to username submitted from the form
                session['username'] = username
                #alert user they were successfully logged in
                flash("you were successfully logged in")
                #send user to dashboard
                return redirect(url_for('dashboard'))
            else:
                #if password does not match username, alert user
                flash("incorrect password")
                #send user back to login
                return redirect(url_for('login'))
        else:
            #if username does not match, alert user
            flash("you were not found in the database please sign up")
            #send user to signup
            return redirect(url_for('signup'))
            

    else:
        #if user is already logged in, send them to the dashboard
        if "username" in session:
            return redirect(url_for("dashboard"))
        #if the method is not post render the login page
        else:
            return render_template('login.html')

@app.route("/signup" , methods=['GET', 'POST'])
def signup():
    #if user submits signup form
    if request.method == "POST":
        #grab data from form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        #check if username is linksafe for profile page
        if re.match("[^A-Za-z0-9]+", username): 
            #if username is not linksafe, alert user
            flash("username must be alphanumeric")
            #refresh signup page
            return redirect(url_for('signup'))
        else:
            #if username is linksafe, check if username is already in database
            found_username = Users.query.filter_by(username=username).first()
            #if username is already in database, alert user
            if found_username:
                flash("username already exists")
                #send user back to login page
                return redirect(url_for('login'))
            else:
                #if username is not in database, set session username to username submitted from form
                session['username'] = username
                #create new user object
                new_user = Users(username, email, password, role)
                # add new user to database
                db.session.add(new_user)
                #commit changes to database
                db.session.commit()
                #alert user they were successfully signed up
                flash(f"you were successfully signed up {new_user.username}" )
                #if user is a technician, send them to the dashboard
                if role == "technician":
                   return redirect(url_for('dashboard'))
                #if user is a customer, send them to the ticket submission page
                else:
                    return redirect(url_for('ticketsubmission'))
    #if the method is not post, render signup page
    else:
        return render_template('signup.html')

@app.route("/logout")
def logout():
    #remove username from session
    session.pop('username', None)
    #alert user they were successfully logged out
    return redirect(url_for('login'))

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    #if user submits selected tickets to be deleted
    if request.method == "POST":
        #grab ticket ids from form
        ticket_ids = request.form.getlist('ticket_id')
        #loop through ticket ids
        for ticket_id in ticket_ids:
            #delete ticket from database
            ticket = Tickets.query.get(ticket_id)
            db.session.delete(ticket)
        #commit changes to database
        db.session.commit()
        #refresh dashboard page
        return redirect(url_for('dashboard'))
    #if the method is not post, render dashboard page
    else:
        #if user is logged in
        if "username" in session:
            #if user is not logged in send them to the login page
            if session['username'] == "USERNAME":
                #alert user they must be logged in to view the dashboard
                flash("please login to view the dashboard")
                return redirect(url_for('login'))
            #if user is logged in as a customer send them to the ticket submission page
            elif Users.query.filter_by(username=session['username']).first().role == "customer":
                #alert user they must be logged in as a technician to view the dashboard
                flash("you must be logged in as a technician to view the dashboard")
                #send user to ticket submission page 
                return redirect(url_for('ticketsubmission'))
            else:
                #if user is logged in as a technician, grab all tickets from database
                tickets = Tickets.query.all()
                #render dashboard page and pass in tickets in to the table
                return render_template("dashboard.html", tickets=tickets)
        else:
            #if user is not logged in alert them they must be logged in to view the dashboard
            flash("you must be logged in to view the dashboard")
            #send user to login page
            return redirect(url_for('login'))

@app.route("/ticketsubmission", methods=['GET', 'POST'])
def ticketsubmission():
    #if user submits ticket submission form
    if request.method == "POST":
        #grab data from form
        ticketAuthor = session['username']
        ticketTitle = request.form['ticketTitle']
        ticketDescription = request.form['ticketDescription']
        ticketPriority = request.form['ticketPriority']
        #create new ticket object
        new_ticket = Tickets(ticketAuthor, ticketTitle, ticketDescription, "open", ticketPriority, "none")
        #add new ticket to database
        db.session.add(new_ticket)
        #commit changes to database
        db.session.commit()
        #alert user ticket was submitted
        flash("ticket submitted")
        #send user to dashboard
        return redirect(url_for('dashboard'))
    else:
        #if the method is not post, render ticket submission page
        if "username" in session:
            #if user is not logged in, send them to the login page
            if session['username'] == "USERNAME":
                #alert user they must be logged in to submit a ticket
                flash("please login to submit a ticket")
                #send user to login page
                return redirect(url_for('login'))
            else:
                #if user is logged in, render ticket submission page
                return render_template('ticketsubmission.html')
        else:
            #if user is not logged in, alert them they must be logged in to submit a ticket
            flash("you must be logged in to submit a ticket")
            #send user to login page
            return redirect(url_for('login'))

@app.route("/profiles/<string:username>")
def profiles(username):
    #grab user data from database
    user = Users.query.filter_by(username=username).first_or_404()
    #render profile page and pass in user data
    return render_template('profile.html', user=user)

@app.route("/tickets/<int:id>", methods=['GET', 'POST'])
def ticket(id):
    #if user submits close or delete button
    if request.method == "POST":
        #grab button pressed from form
        button_pressed = request.form['button']
        #if button pressed is close,
        if button_pressed == "close":
            #grab ticket from database
            ticket = Tickets.query.get_or_404(id)
            #set ticket status to closed
            ticket.status = "closed"
            #set ticket close date to current date
            ticket.date_close = datetime.datetime.now()
            #commit changes to database
            db.session.commit()
        elif button_pressed == "delete":
            #grab ticket from database
            ticket = Tickets.query.get_or_404(id)
            #delete ticket from database
            db.session.delete(ticket)
            #commit changes to database
            db.session.commit()
        #refresh ticket details page
        return redirect(url_for('dashboard'))
        
    else:
        #if the method is not post,
        #grab ticket from database
        ticket = Tickets.query.get_or_404(id)
        #render ticket details page and pass in ticket data
        return render_template("ticketdetails.html", ticket=ticket)

if __name__ == '__main__':
    #create database if not generated
    db.create_all()
    #run app
    app.run(debug=True)