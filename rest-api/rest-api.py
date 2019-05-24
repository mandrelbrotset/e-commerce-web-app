from flask import Flask, request
from flask_hashing import Hashing
import random
from database import Database

app = Flask(__name__)
hashing = Hashing(app)
db = Database()

API_KEY = "193420702d05eb046e6690b2b4a0fc53ec6a52dee3853e568ea55d09526922cf"

@app.route('/signup', methods=["POST"])
def signup():
    try:
        key = request.form["key"]

        if key == API_KEY:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            print(username, email, password)
            salt, hash = generate_salt(password)

            # implement check to see if the email or 
            # username has not been previously used

            if db.connect():
                db.add_user(email, username, hash, salt)
            else:
                print("cannot connect to database")

            return "success"
        else:
            # change to 403 error later
            return "API Key Error"
    except:
        # change to 403 error later
        return "API Key Error"
    
@app.route('/login', methods=["POST"])    
def login():
    try:
        key = request.form["key"]

        if key == API_KEY:
            username = request.form["username"]
            password = request.form["password"]

            print(username, password)
            if db.connect():
                result = db.validate_user(username)

                if result:
                    stored_hash = result[0]
                    stored_salt = result[1]

                    if hashing.check_value(stored_hash, password, stored_salt):
                        return "success"
                else:
                    return "Login error"

            else:
                return "Login error"
        else:
            # change to 403 error later
            return "API Key Error"
    except:
        # change to 403 error later
        return "API Key Error"



def generate_salt(password):
    passw_salt_len = 20
    length = len(password)
    salt_length = passw_salt_len - length
    salt = ""

    for i in range(salt_length):
        r = random.randint(97, 123)
        salt = salt + str(chr(r))

    print(salt)
    hash = hashing.hash_value(password, salt=salt)
    print(hash)

    return salt, hash



if __name__ == "__main__":
    app.run(debug=True, port="5002")