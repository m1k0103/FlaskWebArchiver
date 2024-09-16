from flask import Flask, request, render_template, url_for, abort, redirect, session, render_template_string
from FlaskWebArchiver.func import checkPassword, makeAccount, get_stats_by_username, get_website_from_time, update_stats, generate_code, add_vercode_2db, check_vercode_validity, change_user_password
from FlaskWebArchiver.secret_key import SECRET_KEY, MAIL_ACCOUNT, MAIL_PASS
from FlaskWebArchiver.scrape_website import scrape
from flask_mail import Mail, Message

app = Flask(__name__)

#mail config
app.config["MAIL_SERVER"] = "smtp.office365.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = MAIL_ACCOUNT
app.config["MAIL_PASSWORD"] = MAIL_PASS
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)

app.secret_key = SECRET_KEY

RESET_PASSWORD_SUBJECT = "Hello, you have requested a password reset on the FlaskWebsiteArchiver.\n Please do not share if with anyone.\n\n Your code is: "

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

# ----- FINISHED. DO NOT TOUCH PLEASE. -----
@app.route("/forgotpassword",methods=["GET","POST"])
def forgotpassword():
    if request.method == "GET":
        print("---------- did GET")
        return render_template("forgotpassword.html",stage="stage1")
    elif request.method == "POST":
        if request.form["stage"] == "stage1": # if in first stage
            target_mail = request.form["emailField"]
            msg = Message("Password Reset Code", sender='flaskwebarchiver@outlook.com',recipients=[target_mail])
            code = generate_code()
            msg.body=f"{RESET_PASSWORD_SUBJECT}{code}"
            mail.send(msg)
            print(f"sent mail to {target_mail}")
            add_vercode_2db(code,target_mail)
            return render_template("forgotpassword.html",stage="stage2",mail=target_mail)
        if request.form["stage"] == "stage2": # if in second stage
            input_code = request.form["input_code"]
            target_mail = request.form["mail"]
            if check_vercode_validity(input_code, target_mail) == True:
                return render_template("forgotpassword.html",stage="stage3",mail=target_mail)
            else:
                return render_template("error.html", error="Your input code was not valid. Please try the whole process again.")
        if request.form["stage"] == "stage3": # if finished
            newpassword = request.form["newpassword"]
            target_mail = request.form["mail"]
            change_user_password(newpassword,target_mail)
            return render_template("forgotpassword.html",stage="done")
    


# ----- FINISHED. DO NOT TOUCH PLEASE. -----
@app.route("/dashboard")
def dashboard():
    if "logged_in" in session and session["logged_in"]:
        username = session.get("username")
        stats = get_stats_by_username(username)
        return render_template("dashboard.html", total_searches=stats[0], total_saves=stats[1], saved_sites=stats[2])
    else:
        return render_template("dashboard.html")

# ----- FINISHED. DO NOT TOUCH PLEASE. -----
@app.route("/archive",methods=["GET","POST"])
def archive(): 
    if request.method == "POST": # if authed archive
        if "logged_in" in session and session["logged_in"]:
            url = request.form["archive"]
            update_stats(session["username"], "total_saves", 1)
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

# ----- FINISHED. DO NOT TOUCH PLEASE. -----
@app.route("/timeline",methods=["GET","POST"])
def timeline():
    if request.method == "GET":
        return render_template("timeline.html")
    elif request.method == "POST":
        from_post = request.json["path_to_render"]
        with open(from_post, "r") as f:
            content = f.read()
            return content

# ----- FINISHED. DO NOT TOUCH PLEASE. -----
@app.route("/search",methods=["GET","POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    elif request.method == "POST":
        url = request.form["url"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        website_list = get_website_from_time(url,start_date,end_date)    
        print(website_list)
        try:
            update_stats(session["username"], "total_searches", 1)
        except:
            print("failed to update statistics. user may not be logged in")
            pass
        return render_template("timeline.html", website_list=website_list)


# ----- FINISHED. DO NOT TOUCH PLEASE. -----
@app.route("/loading", methods=["GET", "POST"])
def loading():
    if request.method == "GET":
        return render_template("loading.html")
    elif request.method == "POST":
        from_post = request.json["url"]
        try: # if user is logged in it will use session["username"]
            url = scrape(from_post, session["username"])
        except: # else it will use a blank string
            url = scrape(from_post, "")
    
        print(url)
        with open(url, "r") as f:
            content = f.read()
            return render_template_string(content)
