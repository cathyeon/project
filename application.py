import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///playlist.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return 0
        if not password:
            return 0
        pwhash = generate_password_hash(password)
        insert = db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", username = username, password =pwhash)
        if not insert:
            return apology("Username already exists")
        session["user_id"] = insert
        flash('You have successfully registered.')
        return redirect("/")



@app.route("/input", methods=["GET", "POST"])
def input():
    if request.method == "GET":
        return render_template("input.html")
    else:
    title = request.form.get("title")
    artist = request.form.get("artist")
    input = db.execute("INSERT INTO songs (title, artist) VALUES(:title, :artist)", title = title, artist= artist)

@app.route("/login", methods=["GET", "POST"])
def login():

@app.route("/logout")
def logout():



