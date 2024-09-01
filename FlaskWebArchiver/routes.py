from flask import Flask, request, render_template, url_for, jsonify, redirect, session
from FlaskWebArchiver.func import checkPassword, makeAccount, get_stats
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

# ----- FINISHED. DO NOT TOUCH PLEASE. -----
@app.route("/dashboard")
def dashboard():
    if "logged_in" in session and session["logged_in"]:
        username = session.get("username")
        stats = get_stats(username)
        return render_template("dashboard.html", total_searches=stats[0], total_saves=stats[1])
    else:
        return render_template("dashboard.html")

# ----- FINISHED. DO NOT TOUCH PLEASE. -----
@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "POST": # if authed search
        if "logged_in" in session and session["logged_in"]:
            url = request.form["search"]
            return redirect(url_for("loading"), urltosearch=url)
        else: # if not authed search
            session["free_searches"] -= 1
            if session.get("free_searches") <= 0:
                return render_template("search.html")
            else:
                url = request.form["search"]
                return redirect(url_for("loading"), urltosearch=url)

    elif request.method == "GET":
        if "logged_in" in session and session["logged_in"]:
            return render_template("search.html")
        else:
            if "free_searches" in session and session["free_searches"]:
                pass
            else: 
                session["free_searches"] = 5
            return render_template("search.html", free_searches=session["free_searches"])


    

@app.route("/timeline")
def timeline():
    return render_template("timeline.html")

@app.route("/archive")
def archive():
    return render_template("archive.html")

@app.route("/loading")
def loading():
    return render_template("loading.html")
