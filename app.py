from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

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

def databaseInteract(action):
    # There is going to be 4 different actions. Append, read, write, delete.
    pass


if __name__ == "__main__":
    app.run()