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


@app.route("/")
@login_required
def index():
    """Show list of songs"""
    # Setting a new password
    if request.method == "POST":
        return redirect("/")
    else:
        songs = db.execute("SELECT * FROM songs WHERE user_id = :user_id", user_id=session["user_id"])
        return render_template("index.html", songs=songs)


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
        insert = db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", username = username, password=pwhash)
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
        title = request.form.get("title")
        artist = request.form.get("artist")
        tag = request.form.get("tag")
        tags = request.form.get("tag")
        rating = request.form.get("rating")
        for tag in tags.split(","):
            db.execute("INSERT INTO tags (title, tag, user_id) VALUES (?,?,?)", title, tag, session["user_id"])
        songinput = db.execute("INSERT INTO songs (title, artist, user_id, tag, rating) VALUES (:title, :artist, :user_id, :tag, :rating)", title = title, artist=artist, user_id=session["user_id"], tag = tag, rating = rating)
        if not songinput:
            return apology("did not input song")
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log User In"""

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


@app.route("/logout")
def logout():
    """Log User Out"""
    session.clear()
    return redirect("/")


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
    songs = db.execute("SELECT * FROM songs")
    return render_template("browse.html", songs=songs)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
