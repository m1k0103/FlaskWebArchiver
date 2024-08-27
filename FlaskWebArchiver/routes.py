from flask import Flask, request, render_template, url_for, jsonify, redirect, session
from FlaskWebArchiver.func import checkPassword, makeAccount
from FlaskWebArchiver.secret_key import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/")
def homepage():
    return render_template("homepage.html")

# ----- FINISHED. DO NOT TOUCH PLEASE. -----
@app.route("/signup",methods=["GET","POST"]) 
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if makeAccount(username,password,email) == True: # if account making process in completed correctly (if True)
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("signup"))
    if request.method == "GET":
        if "logged_in" in session and session["logged_in"]:
            return redirect(url_for("dashboard"))
        else:
            return render_template("signup.html")

# ----- FINISHED. DO NOT TOUCH PLEASE. -----
@app.route("/login",methods=["GET", "POST"]) 
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if checkPassword(username, password) == True: # if authenticated
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        else: # if password is wrong
            print(f"{password} not the pass for {username}")
            return redirect(url_for("login"))
    if request.method == "GET": # if logged in and browsed to login then redirect, else nothing
        if "logged_in" in session and session["logged_in"]:
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html")

# ----- FINISHED. DO NOT TOUCH PLEASE. -----
@app.route("/logout",methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route("/forgotpassword")
def forgot_pass():
    return render_template("forgotpassword.html")

@app.route("/dashboard")
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
