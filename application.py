import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


# Function for the index which lists all the songs that the user inputted
@app.route("/")
@login_required
def index():
    """Show list of songs"""
    if request.method == "POST":
        return redirect("/")
    else:
        # Selecting from the databse of songs
        songs = db.execute("SELECT * FROM songs WHERE user_id = :user_id", user_id=session["user_id"])
        return render_template("index.html", songs=songs)

<<<<<<< HEAD

=======
# Function so a new user can register
>>>>>>> d4e64581ae40be3b0b4b99ce6ee89b11a53ad9e4
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        # Returning an apology if no username is inputted
        if not username:
            return apology("Enter valid username")
        # Returning an apology if no password is inputted
        if not password:
            return apology("Enter valid password")
        # Hashing the password
        pwhash = generate_password_hash(password)
        # Storing info into the database
        insert = db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                            username=username, password=pwhash)
        if not insert:
            return apology("Username already exists")
        session["user_id"] = insert
        flash('You have successfully registered.')
        return redirect("/")


@app.route("/input", methods=["GET", "POST"])
def songinput():
    if request.method == "GET":
        return render_template("input.html")
    else:
        # Getting info from form
        title = request.form.get("title")
        artist = request.form.get("artist")
        tag = request.form.get("tag")
        tags = request.form.get("tag")
        rating = request.form.get("rating")
        # Storing tags separated by commas into the tag table
        for tag in tags.split(","):
            db.execute("INSERT INTO tags (title, tag, user_id) VALUES (?,?,?)", title, tag, session["user_id"])
<<<<<<< HEAD
        songinput = db.execute("INSERT INTO songs (title, artist, user_id, tag, rating) VALUES (:title, :artist, :user_id, :tag, :rating)", title = title, artist=artist, user_id=session["user_id"], tag = tag, rating = rating)
=======
        # Inputting info into the database
        songinput = db.execute("INSERT INTO songs (title, artist, user_id, tag, rating) VALUES (:title, :artist, :user_id, :tag, :rating)",
                               title=title, artist=artist, user_id=session["user_id"], tag=tag, rating=rating)
>>>>>>> d4e64581ae40be3b0b4b99ce6ee89b11a53ad9e4
        if not songinput:
            return apology("did not input song")
        else:
            flash('You have inputted a song!')
        return redirect("/")

<<<<<<< HEAD

=======
# Function so that a user can log in
>>>>>>> d4e64581ae40be3b0b4b99ce6ee89b11a53ad9e4
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log User In"""
    # Taken from CS50 Finance Problem Set
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Please provide a username", 403)
        elif not request.form.get("password"):
            return apology("Please provide a password", 403)
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

# Function so that a user can log out
@app.route("/logout")
def logout():
    """Log User Out"""
    # Taken from CS50 Finance Problem Set
    session.clear()
    return redirect("/")


<<<<<<< HEAD
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    personaltags = db.execute("SELECT tag, count(tag) AS common FROM tags WHERE user_id=:user_id GROUP BY tag ORDER BY common DESC LIMIT 1", user_id=session["user_id"])
    row={}
    for row in personaltags:
       pop = row["tag"]
    tags = db.execute("SELECT * FROM songs WHERE tag = :common", common = pop)

    #ratings = db.execute("SELECT * FROM songs WHERE user_id=:user_id", user_id= session["user_id"])
    #others = db.execute("SELECT * FROM songs WHERE user_id!=:user_id", user_id= session["user_id"])

    #for i in others:
    #    for j in ratings:
    #        if i["rating"] == j["rating"]:
    #            recommend["title"] = j["title"]
    #            recommend["artist"] = j["artist"]

    return render_template("recommend.html", tags=tags)


@app.route("/browse", methods=["GET", "POST"])
def browse():
=======
# Function that gives song recommendations
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    """Recommends songs"""
    # Selects the most common tag of the songs that you inputted
    personaltags = db.execute(
        "SELECT tag, count(tag) AS common FROM tags WHERE user_id=:user_id GROUP BY tag ORDER BY common DESC LIMIT 1", user_id=session["user_id"])
    row = {}
    # Finds every song in the database with that tag
    for row in personaltags:
        pop = row["tag"]
    tags = db.execute("SELECT * FROM songs WHERE tag = :common", common=pop)
    return render_template("recommend.html", tags=tags)

# Function that allows users to see every songs in the database and search it up on youtube
@app.route("/browse", methods=["GET", "POST"])
def browse():
    """Lists all the songs"""
>>>>>>> d4e64581ae40be3b0b4b99ce6ee89b11a53ad9e4
    songs = db.execute("SELECT * FROM songs")
    return render_template("browse.html", songs=songs)

# Taken directly from CS50 Finance


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

