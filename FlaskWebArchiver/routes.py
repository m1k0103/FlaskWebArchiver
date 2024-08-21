from flask import Flask, request, render_template
import sqlite3, os
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login",methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/forgotpassword")
def forgot_pass():
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

if __name__ == "__main__":
    app.run()