from flask import Flask, request, render_template, url_for, jsonify, redirect, session, render_template_string
from FlaskWebArchiver.func import checkPassword, makeAccount, get_stats
from FlaskWebArchiver.secret_key import SECRET_KEY
from FlaskWebArchiver.scrape_website import scrape

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
@app.route("/archive",methods=["GET","POST"])
def archive(): 
    if request.method == "POST": # if authed archive
        if "logged_in" in session and session["logged_in"]:
            url = request.form["archive"]
            return render_template("loading.html", urltoarchive=url)
        else: # if not authed archive
            session["free_archives"] -= 1
            if session.get("free_archives") <= 0:
                return render_template("archive.html")
            else:
                url = request.form["archive"]
                return render_template("loading.html", urltoarchive=url)

    elif request.method == "GET":
        if "logged_in" in session and session["logged_in"]:
            return render_template("archive.html")
        else:
            if "free_archives" in session and session["free_archives"]:
                pass
            else: 
                session["free_archives"] = 5
            return render_template("archive.html", free_archives=session["free_archives"])


@app.route("/timeline")
def timeline():
    return render_template("timeline.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/loading", methods=["GET", "POST"])
def loading():
    if request.method == "GET":
        return render_template("loading.html")
    elif request.method == "POST":
        from_post = request.json["url"]
        url = scrape(from_post)
        print(url)
        with open(url, "r") as f:
            content = f.read()
            return render_template_string(content)
    