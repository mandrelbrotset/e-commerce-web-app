from flask import Flask, request
from flask_hashing import Hashing
import random
import json
from database import Database

app = Flask(__name__)
hashing = Hashing(app)
db = Database()

API_KEY = "193420702d05eb046e6690b2b4a0fc53ec6a52dee3853e568ea55d09526922cf"

# Error codes
ERR_1 = "API Key Required"
ERR_2 = "Username not available"
ERR_3 = "Failed to create account"
ERR_4 = "Unable to add item"
ERR_5 = "Invalid method"


@app.route('/signup', methods=["POST"])
def user_signup():
    if request.method == "POST":
        if "key" in request.form:
            key = request.form["key"]

            if key == API_KEY:
                # get data from the request
                f_name = request.form["first_name"]
                l_name = request.form["last_name"]
                email = request.form["email"]
                password = request.form["password"]
                
                # capitalize first letter of names
                f_name = f_name.title()
                l_name = l_name.title()
                # convert email to lower case
                email = email.lower()

                # check if username is available
                if db.check_user(email):
                    # generate hash for the password
                    salt, hash = generate_hash(password)

                    if db.add_user(email, f_name, l_name, hash, salt): 
                        return json.dumps({"result" : "success"})
                    else:
                        return json.dumps({"result" : ERR_3})
                else:
                    return json.dumps({"result" : ERR_2})
            else:
                # change to 403 error later
                return json.dumps({"result" : ERR_1})
        else:
            # change to 403 error later
            return json.dumps({"result" : ERR_1})

    return json.dumps({"result" : ERR_5})


@app.route('/admin_signup', methods=["POST"])
def admin_signup():
    if request.method == "POST":
        if "key" in request.form:
            key = request.form["key"]

            if key == API_KEY:
                # get data from the request
                f_name = request.form["first_name"]
                l_name = request.form["last_name"]
                email = request.form["email"]
                password = request.form["password"]
                
                # capitalize first letter of names
                f_name = f_name.title()
                l_name = l_name.title()
                # convert email to lower case
                email = email.lower()

                # check if username is available
                if db.check_admin(email):
                    # generate hash for the password
                    salt, hash = generate_hash(password)

                    if db.add_admin(email, f_name, l_name, hash, salt): 
                        return json.dumps({"result" : "success"})
                    else:
                        return json.dumps({"result" : ERR_3})
                else:
                    return json.dumps({"result" : ERR_2})

            else:
                # change to 403 error later
                return json.dumps({"result" : ERR_1})
        else:
            # change to 403 error later
            return json.dumps({"result" : ERR_1})

    return json.dumps({"result" : ERR_5})

@app.route('/login', methods=["POST"])
def user_login():
    if request.method == "POST":
        if "key" in request.form:
            key = request.form["key"]

            if key == API_KEY:
                # get data from the request
                email = request.form["email"]
                password = request.form["password"]

                # convert inputted email to lower case
                email = email.lower()

                result = db.validate_user(email)

                if result:
                    stored_hash = result[0]
                    stored_salt = result[1]
                    f_name = result[2]
                    l_name = result[3]

                    if hashing.check_value(stored_hash, password, salt=stored_salt):
                        ret = {"result" : "success",
                               "first_name": f_name,
                               "last_name": l_name}
                        return json.dumps(ret)
                    else:
                        return json.dumps({"result" : "Login error"})
                else:
                    return json.dumps({"result" : "Login error"})
            else:
                # change to 403 error later
                return json.dumps({"result" : ERR_1})
        else:
            # change to 403 error later
            return json.dumps({"result" : ERR_1})

    return json.dumps({"result" : ERR_5})


@app.route('/admin_login', methods=["POST"])
def admin_login():
    if request.method == "POST":
        if "key" in request.form:
            key = request.form["key"]

            if key == API_KEY:
                # get data from the request
                email = request.form["email"]
                password = request.form["password"]

                # convert inputted email to lower case
                email = email.lower()

                result = db.validate_admin(email)

                if result:
                    stored_hash = result[0]
                    stored_salt = result[1]
                    f_name = result[2]
                    l_name = result[3]

                    if hashing.check_value(stored_hash, password, salt=stored_salt):
                        ret = json.dumps({"result" : "success",
                                          "first_name": f_name,
                                          "last_name": l_name})
                        return ret
                else:
                    return json.dumps({"result" : "Login error"})
            else:
                # change to 403 error later
                return json.dumps({"result" : ERR_1})
        else:
            # change to 403 error later
            return json.dumps({"result" : ERR_1})

    return json.dumps({"result" : ERR_5})


@app.route('/add_item', methods=["POST"])
def add_item():
    if request.method == "POST":
        if "key" in request.form:
            key = request.form["key"]

            if key == API_KEY:
                # get data from the request
                name = request.form["name"]
                quantity = request.form["quantity"]
                tags = request.form["tags"]
                description = request.form["description"]
                price = request.form["price"]
                image_url = request.form["image_url"]

                if db.add_item(name, quantity, tags, description, price, image_url):
                    return json.dumps({"result" : "success"})
                else:
                    return json.dumps({"result" : ERR_4})

    return json.dumps({"result" : ERR_5})


@app.route('/get_items', methods=["POST"])
def get_items():
    if request.method == "POST":
        if "key" in request.form:
            key = request.form["key"]

            if key == API_KEY:
                items = db.get_items()
                products = []

                for item in items:
                    products.append([item[0], item[1], item[2], item[3],\
                     item[4], float(item[5]), item[6]])

                ret = {"result" : "success",
                       "items" : products}
                return json.dumps(ret)

    return json.dumps({"result" : ERR_5})


@app.route('/item_by_id', methods=["POST"])
def item_by_id():
    if request.method == "POST":
        item_id = request.form["item_id"]

        item = db.item_by_id(item_id)
        product = [item[0], item[1], item[2], item[3], item[4], float(item[5]), item[6]]

        ret = {"result" : "success",
               "item"   : product}

        return json.dumps(ret)

    return json.dumps({"result" : ERR_5})


@app.route('/add_to_cart', methods=["POST"])
def add_to_cart():
    if request.method == "POST":
        if "key" in request.form:
            key = request.form["key"]

            # check for API Key
            if key == API_KEY:
                email = request.form["email"]
                quantity = int(request.form["quantity"])
                item_id = request.form["item_id"]

                # if the user has the item in stock already
                if db.in_cart(email, item_id) and db.item_quantity(item_id) >= quantity + 1:
                    # increase the qunatity in the cart
                    db.increase_quantity(email, item_id)
                    return json.dumps({"result" : "success"})
                else:
                    # check if there is enough qunatity in stock
                    if quantity < 1:
                        return json.dumps({"result" : "Quantity must be at least 1"})
                    elif quantity > db.item_quantity(item_id):
                        return json.dumps({"result" : "Not enough quantity in stock"})
                    else:
                        db.add_to_cart(email, item_id, quantity)
                        return json.dumps({"result" : "success"})
                            
    return json.dumps({"result" : ERR_5})


@app.route('/cart', methods=["POST"])
def cart():
    if request.method == "POST":
        if "key" in request.form:
            key = request.form["key"]

            # check for API Key
            if key == API_KEY:
                email = request.form["email"]

                # get item_id, quantity and price of the items in the users cart
                value = db.get_user_cart(email)

                cart = []

                #
                if value:
                    for val in value:
                        # get more details about the cart item
                        item = db.item_by_id(val[0])
                        cart.append({"item_id":val[0], "quantity":val[1], "price":float(item[5]), 
                                     "name":item[1], "image_url":item[6]})

                    ret = {"result" : "success",
                           "cart" : cart}

                    return json.dumps(ret)
                else:
                    return json.dumps({"result" : "empty"})

    return json.dumps({"result" : ERR_5})
                

@app.route('/account', methods=["POST"])
def account():
    if request.method == "POST":
        if 'key' in request.form:
            key = request.form["key"]

            # check for API Key
            if key == API_KEY:
                email = request.form["email"]
                f_name, l_name = db.user_details(email)

                return json.dumps({"result": "success",
                                   "first_name" : f_name,
                                   "last_name" : l_name})
            else:
                return json.dumps({"result" : "empty"})

    return json.dumps({"result" : ERR_5})


@app.route('/change_name', methods=["POST"])
def change_name():
    if request.method == "POST":
        if 'key' in request.form:
            key = request.form["key"]

            # check for API Key
            if key == API_KEY:
                email = request.form["email"]
                first_name = ""
                last_name = ""

                if 'first_name' in request.form:
                    first_name = request.form["first_name"]

                if 'last_name' in request.form:
                    last_name = request.form["last_name"]

                if db.change_name(email, first_name, last_name):
                    return json.dumps({"result" : "success"})

                return json.dumps({"result" : "failed"})
    
    return json.dumps({"result" : ERR_5})


@app.route('/change_password', methods=["POST"])
def change_password():
    if request.method == "POST":
        if 'key' in request.form:
            key = request.form["key"]

            # check for API Key
            if key == API_KEY:
                email = request.form["email"]
                password = request.form["password"]

                # generate hash for the password
                salt, password_hash = generate_hash(password)

                # change password hash and salt in database
                if db.change_password(email, password_hash, salt):
                    return json.dumps({"result" : "success"})

                return json.dumps({"result" : "failed"})
    
    return json.dumps({"result" : ERR_5})


@app.route('/delete_account', methods=["POST"])
def delete_account():
    if request.method == "POST":
        if 'key' in request.form:
            key = request.form["key"]

            # check for API Key
            if key == API_KEY:
                email = request.form["email"]
                
                if db.delete_user(email):
                    return json.dumps({"result" : "success"})

                return json.dumps({"result" : "failed"})

    return json.dumps({"result" : ERR_5})


@app.route('/admin_account', methods=["POST"])
def admin_account():
    if request.method == "POST":
        if 'key' in request.form:
            key = request.form["key"]

            # check for API Key
            if key == API_KEY:
                email = request.form["email"]
                f_name, l_name = db.admin_details(email)

                return json.dumps({"result": "success",
                                   "first_name" : f_name,
                                   "last_name" : l_name})
            else:
                return json.dumps({"result" : "empty"})

    return json.dumps({"result" : ERR_5})


@app.route('/change_admin_name', methods=["POST"])
def change_admin_name():
    if request.method == "POST":
        if 'key' in request.form:
            key = request.form["key"]

            # check for API Key
            if key == API_KEY:
                email = request.form["email"]
                first_name = ""
                last_name = ""

                if 'first_name' in request.form:
                    first_name = request.form["first_name"]

                if 'last_name' in request.form:
                    last_name = request.form["last_name"]

                if db.change_admin_name(email, first_name, last_name):
                    return json.dumps({"result" : "success"})

                return json.dumps({"result" : "failed"})
    
    return json.dumps({"result" : ERR_5})


@app.route('/change_admin_password', methods=["POST"])
def change_admin_password():
    if request.method == "POST":
        if 'key' in request.form:
            key = request.form["key"]

            # check for API Key
            if key == API_KEY:
                email = request.form["email"]
                password = request.form["password"]

                # generate hash for the password
                salt, password_hash = generate_hash(password)

                # change password hash and salt in database
                if db.change_admin_password(email, password_hash, salt):
                    return json.dumps({"result" : "success"})

                return json.dumps({"result" : "failed"})
    
    return json.dumps({"result" : ERR_5})


@app.route('/delete_admin_account', methods=["POST"])
def delete_admin_account():
    if request.method == "POST":
        if 'key' in request.form:
            key = request.form["key"]

            # check for API Key
            if key == API_KEY:
                email = request.form["email"]
                
                if db.delete_admin(email):
                    return json.dumps({"result" : "success"})

                return json.dumps({"result" : "failed"})

    return json.dumps({"result" : ERR_5})

def generate_hash(password):
    passw_salt_len = 20
    length = len(password)
    salt_length = passw_salt_len - length
    salt = ""

    for i in range(salt_length):
        r = random.randint(97, 122)
        salt = salt + str(chr(r))

    hash = hashing.hash_value(password, salt=salt)

    return salt, hash


if __name__ == "__main__":
    app.run(debug=True, port="5002")