import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Dollar sign filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create the SQL database
db = SQL("sqlite:///project.db")


@app.route("/")
@login_required
def index():
    # Show the homepage(once user is logged in)
    row = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
    username = row[0]["username"]
    return render_template("index.html", username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    
    # If get, display page
    if request.method == "GET":
        return render_template("register.html")
    
    # If Post, update table
    if request.method == "POST":
        
        # Check for errors
        if not request.form.get("username"):
            return apology("Please enter a username")
        
        if not request.form.get("password"):
            return apology("Please enter a password")
            
        if not request.form.get("confirm"):
            return apology("Please confirm your password")
            
        # Check to make sure password & confirmation match 
        if request.form.get("password") != request.form.get("confirm"):
            return apology("Your password and confirmation do not match")
        
        # hash the password
        password = generate_password_hash(request.form.get("password"))
        
        # Update table with information
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), password)
        
        return redirect("/")
        
        
@app.route("/login", methods=["GET", "POST"])
def login():
    
    # Forget any user_id
    session.clear()
    
    # If get, show login form
    if request.method == "GET":
        return render_template("login.html")
        
    # If post, submit info
    if request.method == "POST":
        
        # Check for errors
        if not request.form.get("username"):
            return apology("Please enter a username")
            
        if not request.form.get("password"):
            return apology("Please enter a password")
            
        # Get info about user from the db
        row = db.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))
        
        # Check to see if user exists
        if len(row) != 1 or not check_password_hash(row[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")
            
        # Remember this user
        session["user_id"] = row[0]["id"]
        # Add into db
        
        return redirect("/")
        
@app.route("/logout")
def logout():
    
    # Forget any cookies/session id
    session.clear()
    
    # Redirect user to login
    return redirect("/login")
  
    


@app.route("/profile", methods=["GET", "POST"])
def profile():
    # Show the user's profile
    if request.method == "GET":
        row = db.execute("SELECT * FROM profile WHERE profile_id=?", session["user_id"])
        if len(row) != 1:
            return redirect("/change")
        return render_template("profile.html", row=row)
    
    #if request.method == "POST":
        #return redirect("/change")
        

@app.route("/name", methods=["GET", "POST"])
def name():
    if request.method=="GET":
        return render_template("name.html")
        
    if request.method=="POST":
        if not request.form.get("name"):
            return apology("Please update your name")
        db.execute("UPDATE profile SET name=? WHERE profile_id=?", request.form.get("name"), session["user_id"])
        return redirect("/profile")
        
@app.route("/age", methods=["GET", "POST"])
def age():
    if request.method == "GET":
        return render_template("age.html")
    
    if request.method == "POST":
        if not request.form.get("age"):
            return apology("Please upadte your age")
        db.execute("UPDATE profile SET age=? WHERE profile_id=?", request.form.get("age"), session["user_id"])
        return redirect("/profile")
        
@app.route("/email", methods=["GET", "POST"])
def email():
    if request.method == "GET":
        return render_template("email.html")
    
    if request.method == "POST":
        if not request.form.get("email"):
            return apology("Please update your email address")
        db.execute("UPDATE profile SET email=? WHERE profile_id=?", request.form.get("email"), session["user_id"])
        
        
@app.route("/phone", methods=["GET", "POST"])
def phone():
    if request.method == "GET":
        return render_template("phone.html")
    
    if request.method == "POST":
        if not request.form.get("phone"):
            return apology("Please update your phone number")
        db.execute("UPDATE profile SET phone=? WHERE profile_id=?", request.form.get("phone"), sesesion["user_id"])
        return redirect("/profile")

@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "GET":
        return render_template("about.html")
    
    if request.method == "POST":
        if not request.form.get("about"):
            return apology("Please update your 'About Me' section")
        db.execute("UPDATE profile SET bio=? WHERE profile_id=?", request.form.get("about"), session["user_id"])
        return redirect("/profile")

@app.route("/change", methods=["GET", "POST"])
def change():
    # Allow user to change profile
    if request.method == "GET":
        return render_template("change.html")
        
    if request.method == "POST":
        if not request.form.get("name"):
            return apology("Please update your name")
        
        if not request.form.get("age"):
            return apology("Please update your age")
        
        if not request.form.get("email"):
            return apology("Please update your email")
        
        if not request.form.get("phone"):
            return apology("Please update your phone number")
        
        if not request.form.get("bio"):
            return apology("Please update your About Me section")
        
        row = db.execute("SELECT * FROM profile WHERE profile_id=?", session["user_id"])
        if len(row) != 1:
            db.execute("INSERT INTO profile (name, age, email, phone, bio, profile_id) VALUES (?, ?, ?, ?, ?, ?)", request.form.get("name"), request.form.get("age"), request.form.get("email"), request.form.get("phone"), request.form.get("bio"), session["user_id"])
        
        else:
            db.execute("UPDATE profile SET name=?, age=?, email=?, phone=?, bio=? WHERE profile_id=?", request.form.get("name"), request.form.get("age"), request.form.get("email"), request.form.get("phone"), request.form.get("bio"), session["user_id"])
        
        return redirect("/profile")

@app.route("/plist", methods=["GET", "POST"])
def plist():
    # Take user to their prayer list
    # if method is get
    if request.method == "GET":
        row = db.execute("SELECT * FROM plist WHERE plist_id=?", session["user_id"])
        return render_template("plist.html", row=row)
        
    # Allow user to change / update their prayer list
    # if request method is post
    if request.method == "POST":
        # Check for errors
        if not request.form.get("request"):
            return apology("Please include your prayer request")
        db.execute("INSERT INTO plist (request, name, date, plist_id) VALUES (?, ?, ?, ?)", request.form.get("request"), request.form.get("name"), request.form.get("date"), session["user_id"])
        return redirect("/plist")
            

@app.route("/sort", methods=["GET", "POST"])
def sort():
    # If method is post:
    if request.method == "POST":
        # Check for errors
        if not request.form.get("query"):
            return apology("Please enter a name to sort by")
        
        # Query db for the requested name
        row = db.execute("SELECT * FROM plist WHERE name=? AND plist_id=?", request.form.get("query"), session["user_id"])
        return render_template("sort.html", row=row)
        
    

@app.route("/budget", methods=["GET", "POST"])
def budget():
    # If method is get, display budget
    if request.method == "GET":
        # Check to see if user has budget info
        row = db.execute("SELECT * FROM budgetuse WHERE budgetuse_id=?", session["user_id"])
        # If first time, ask for their balance
        if len(row) < 1:
            return redirect("/setup")
        balanceuse = row[0]["balance"]
        # Otherwise, just show the balance + budget
        return render_template("budget.html", row=row, balanceuse=balanceuse)
    # Allow them to update their budget 
    if request.method == "POST":
        # Error checking
        if not request.form.get("type"):
            return apology("Please enter a transaction type")
        if not request.form.get("amount"):
            return apology("Please enter an amount")
        if not request.form.get("description"):
            return apology("Please enter a description")
        if not request.form.get("date"):
            return apology("Please enter a date")
        
        
        # Find current balance
        row = db.execute("SELECT * FROM budgetuse WHERE budgetuse_id=?", session["user_id"])
        balance = row[0]["balance"]
        
        # Add or subtract value to get new balance
        if request.form.get("type") == "increase":
            newbalance = balance + int(request.form.get("amount"))
            # Insert into database
            db.execute("INSERT INTO budgetuse (balance, type, amount, description, date, budgetuse_id) VALUES (?, ?, ?, ?, ?, ?)", newbalance, "+", request.form.get("amount"), request.form.get("description"), request.form.get("date"), session["user_id"])
            db.execute("UPDATE budgetuse SET balance=? WHERE budgetuse_id=?", newbalance, session["user_id"])
            
        if request.form.get("type") == "decrease":
            newbalance = balance - int(request.form.get("amount"))
            # Insert into database
            db.execute("INSERT INTO budgetuse (balance, type, amount, description, date, budgetuse_id) VALUES (?, ?, ?, ?, ?, ?)", newbalance, "-", request.form.get("amount"), request.form.get("description"), request.form.get("date"), session["user_id"])
            db.execute("UPDATE budgetuse SET balance=? WHERE budgetuse_id=?", newbalance, session["user_id"])
        
        
        return redirect("/budget")
            
@app.route("/setup", methods=["GET", "POST"])
def setup():
    # If method is get, display pagge
    if request.method == "GET":
        return render_template("setup.html")
    
    # If method is post, submit info
    if request.method == "POST":
        # Check for errors
        if not request.form.get("balance"):
            return aplogy("Please specify your current balance")
        
        # Insert current balance into db
        db.execute("INSERT INTO budgetuse (balance, budgetuse_id) VALUES (?, ?)", request.form.get("balance"), session["user_id"])
        return redirect("/budget")
        

@app.route("/birthdays", methods=["GET", "POST"])
def birthdays():
    # If method is Get:
    if request.method == "GET":
        # Show user their birthdays list
        row = db.execute("SELECT * FROM birthdays WHERE birth_id=?", session["user_id"])
        return render_template("birthdays.html", row=row)
    # If method is post:
    if request.method == "POST":
        # Check for errors
        if not request.form.get("name"):
            return apology("Please enter the name")
        if not request.form.get("date"):
            return apology("Please enter the date")
        row = db.execute("SELECT * FROM birthdays WHERE name=? AND birth_id=?", request.form.get("name"), session["user_id"])
        if len(row) == 1:
            return apology("You have already logged this person's birthday")
        # Allow them to add dates/names to their birthday list
        db.execute("INSERT INTO birthdays (name, date, birth_id) VALUES (?, ?, ?)", request.form.get("name"), request.form.get("date"), session["user_id"])
        
    return redirect("/birthdays")
    
@app.route("/sortb", methods=["GET", "POST"])
def sortb():
    # If requested via post
    if request.method == "POST":
        # check for errors
        if not request.form.get("date"):
            return apology("Please enter a date to sort by")
        
        # query db
        row = db.execute("SELECT * FROM birthdays WHERE date=? AND birth_id=?", request.form.get("date"), session["user_id"])
        return render_template("sortb.html", row=row)


#@app.route("/deletedate", methods=["GET", "POST"])
#def deletedate():
    #if request.method == "POST":
        # Need to figure out a way to remove unwanted entries
        # This method doesn't work as the request.form.get("") statements don't connect to the original form
        # How can I connect to / get the info about the row that is to be deleted....?
        #db.execute("DELETE FROM birthdays WHERE name=? AND date=? AND birth_id=?", request.form.get("name"), request.form.get("date"), session["user_id"])
        
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
