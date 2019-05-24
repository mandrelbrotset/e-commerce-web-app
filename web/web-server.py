from flask import Flask, request, render_template, flash, session, redirect, url_for
import requests as re

app = Flask(__name__)
app.secret_key = "0reiyzujsn048ri7nsaej2cpdgildcbdspdbqyee10svy6nmom"

# Rest API 
API_ENDPOINT = "http://127.0.0.1:5002/"
API_KEY = "193420702d05eb046e6690b2b4a0fc53ec6a52dee3853e568ea55d09526922cf"


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if len(username) > 0 and len(email) > 0 and len(password) > 8:
            endpoint = API_ENDPOINT + "signup"
            params = {"username": username,
                    "email": email,
                    "password": password}

            params["key"] = API_KEY
            response = re.post(url=endpoint, data=params)

            if response.text == "success":
                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for("dashboard"))
        else:
            if len(username) <= 0:
                flash("You must enter a username")
            if len(email) <= 0:
                flash("You must enter an email")
            if len(password) < 8:
                flash("Password must length requirements")
            

    return render_template("signup.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        endpoint = API_ENDPOINT + "login"
        params = {"username": username,
                  "password": password}

        params["key"] = API_KEY
        response = re.post(url=endpoint, data=params)

        if response.text == "success":
            session['logged_in'] = True
            session['username'] = username

            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password. Please try again!"

    return render_template("login.html", error=error)

@app.route('/dashboard')
def dashboard():
    username = session['username']
    if session['logged_in'] and len(username) > 0:
        return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)