import os

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
import json
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)

db = SQL("sqlite:///todolist.db")

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show to-do list"""
    if request.method == "GET":
        entries_dict = db.execute("SELECT task_name, status FROM tasks WHERE user_id=?", session["user_id"])
        entries = []
        for entry in entries_dict:
            entries.append((entry["task_name"], entry["status"]))
        return render_template("index.html", entries=entries)

    new_task = request.form.get("new_task")

    if new_task.strip():
        db.execute("INSERT INTO tasks (user_id, task_name) VALUES (?, ?)", session["user_id"], new_task)
    entries = db.execute("SELECT task_name, status FROM tasks WHERE user_id=?", session["user_id"])

    return render_template("index.html", entries=entries)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", user_error="* Please enter username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", pass_error="* Please enter password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", pass_error="* Password and username do not match")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register for a new account"""
    if request.method == "GET":
        return render_template("register.html")

    # Ensure username was submitted
    username = request.form.get("username")
    if not username:
        return render_template("register.html", user_error="* Please enter a username")

    # Check whether username has been taken
    user_test = db.execute("SELECT username FROM users WHERE username = ?", username)
    if len(user_test) != 0:
        return render_template("register.html", user_error="* Username taken")

    # Check validity of password
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    if not password:
        return render_template("register.html", pass_error="* Please enter a password")
    elif password != confirmation:
        return render_template("register.html", conf_error="* Passwords do not match")

    # Add username and password hash into database 'users'
    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
    
    user = db.execute("SELECT id FROM users WHERE username = ?", username)
    session["user_id"] = user[0]["id"]
    return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form 
    return redirect("/")

@app.route("/update-todo/<task_id>", methods=["POST"])
def updateToDo(task_id):
    """Updates status of task: Completed/Incomplete"""
    
    status = db.execute("SELECT status FROM tasks WHERE user_id = ? AND task_name = ?", session["user_id"], task_id)
    if status[0]["status"] == "Incomplete":
        db.execute("UPDATE tasks SET status = 'Completed' WHERE user_id = ? AND task_name = ?", session["user_id"], task_id)
    else:
        db.execute("UPDATE tasks SET status = 'Incomplete' WHERE user_id = ? AND task_name = ?", session["user_id"], task_id)

    return redirect("/")
