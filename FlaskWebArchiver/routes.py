from flask import Flask, request, render_template, url_for, jsonify, redirect, session
import os, sqlite3
from markupsafe import escape
from FlaskWebArchiver.func import checkPassword

app = Flask(__name__)
app.secret_key = b"_test5#5#5[2#2#156kzz'xw]gsd_a"

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
    return render_template("signup.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if checkPassword(username, password) == True:
            session["logged_in"] = True
            return redirect(url_for("homepage"))
        else:
            return redirect(url_for("login"))
    else:
        return render_template("login.html")

@app.route("/logout",methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('homepage'))

@app.route("/forgotpassword")
def forgot_pass():
    if session[]
    return render_template("forgotpassword.html")

@app.route("/user/<string:username>")
def dashboard():
    return render_template("dashboard.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/timeline")
def timeline():
    return render_template("timeline.html")

@app.route("/archive")
def archive():
    return render_template("archive.html")

@app.route("/loading")
def loading():
    return render_template("loading.html")

@app.route("/debug")
def test():
    return render_template("test.html")
