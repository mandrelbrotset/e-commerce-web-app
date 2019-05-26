from flask import Flask, request
from flask_hashing import Hashing
import random
from database import Database

app = Flask(__name__)
hashing = Hashing(app)
db = Database()

API_KEY = "193420702d05eb046e6690b2b4a0fc53ec6a52dee3853e568ea55d09526922cf"

# Error codes
ERR_1 = "API Key Required"
ERR_2 = "Username not available"
ERR_3 = "Failed to create account"

@app.route('/signup', methods=["POST"])
def signup():
    if request.method == "POST":
        if "key" in request.form:
            key = request.form["key"]

            if key == API_KEY:
                username = request.form["username"]
                email = request.form["email"]
                password = request.form["password"]

                print(username, email, password)
                salt, hash = generate_salt(password)

                # check if username is available
                if db.check_user(username):
                    if db.add_user(email, username, hash, salt):
                        return "success"
                    else:
                        return ERR_3
                else:
                    return ERR_2
            else:
                # change to 403 error later
                return ERR_1
        else:
            # change to 403 error later
            return ERR_1
    
@app.route('/login', methods=["POST"])    
def login():
    if request.method == "POST":
        if "key" in request.form:
            key = request.form["key"]

            if key == API_KEY:
                username = request.form["username"]
                password = request.form["password"]

                print(username, password)
                result = db.validate_user(username)

                print(result)
                if result:
                    stored_hash = result[0]
                    stored_salt = result[1]

                    hash = hashing.hash_value(password, salt=stored_salt)
                    print(hash)

                    if hashing.check_value(stored_hash, password, salt=stored_salt):
                        return "success"
                else:
                    return "Login error"
            else:
                # change to 403 error later
                return ERR_1
        else:
            # change to 403 error later
            return ERR_1


def generate_salt(password):
    passw_salt_len = 20
    length = len(password)
    salt_length = passw_salt_len - length
    salt = ""

    for i in range(salt_length):
        r = random.randint(97, 122)
        salt = salt + str(chr(r))

    print(salt)
    hash = hashing.hash_value(password, salt=salt)
    print(hash)

    return salt, hash



if __name__ == "__main__":
    app.run(debug=True, port="5002")