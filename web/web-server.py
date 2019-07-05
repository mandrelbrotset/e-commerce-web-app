from flask import Flask, request, render_template, flash, session, redirect, \
    url_for, send_from_directory
import requests as re
from werkzeug.utils import secure_filename
import json
import os


# Rest API endpoint
API_ENDPOINT = "http://127.0.0.1:5002/"
API_KEY = "193420702d05eb046e6690b2b4a0fc53ec6a52dee3853e568ea55d09526922cf"
UPLOAD_FOLDER = "static/images"

# flask config
app = Flask(__name__, static_folder='static')
app.secret_key = "0reiyzujsn048ri7nsaej2cpdgildcbdspdbqyee10svy6nmom"


@app.route('/')
def home():
    return render_template('home.html')

    
@app.route('/signup', methods=["GET", "POST"])
def user_signup():
    error = []

    if request.method == "POST":
        # get data from html form
        f_name = request.form["first_name"]
        l_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]

        if len(f_name) > 0 and len(l_name) > 0 and len(email) > 0 and len(password) > 6:
            # Rest API endpoint
            endpoint = API_ENDPOINT + "signup"

            # dictionary to be used as POST request data
            params = {"first_name": f_name,
                      "last_name" : l_name,
                      "email": email,
                      "password": password,
                      "key" : API_KEY}

            # make a POST request to the Rest API
            response = re.post(url=endpoint, data=params)
            response = json.loads(response.text)

            # if API call succeeds
            if response['result'] == "success":
                # save variables in session storage
                session['logged_in'] = True
                session['email'] = email
                # save first name in  session storage with first letter capitalized
                session['first_name'] = f_name.title()
                # redirect to dashboard
                return redirect(url_for("home"))
            else:
                error = [response['result']]

        else:
            if len(f_name) <= 0:
                error.append("You must enter a first name")
            if len(l_name) <= 0:
                error.append("You must enter a last name")
            if len(email) <= 0:
                error.append("You must enter an email")
            if len(password) < 6:
                error.append("Password must meet length requirements")
            
    return render_template("signup.html", error=error)


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Rest API endpoint
        endpoint = API_ENDPOINT + "sign_in"

        params = {"email": email,
                  "password": password}

        # store API key in post request data
        params["key"] = API_KEY
        # make a POST request to the Rest API
        response = re.post(url=endpoint, data=params)
        # convert result from JSON to python dictionary
        response = json.loads(response.text)

        # if API call succeeds
        if response['result'] == "success":
            # save email in session storage
            session['email'] = email
            # save first name in  session storage with first letter capitalized
            session['first_name'] = response['first_name'].title()
            session['logged_in'] = True

            session.pop('admin_logged_in', None)
            # redirect to dashboard
            return redirect(url_for("home"))
        
        else:
            error = "Invalid username or password!"

    if "logged_in" in session:
        if session['logged_in']:
            return redirect(url_for("home"))

    return render_template("signin.html", error=error)


@app.route('/signout')
def signout():
    session.pop('logged_in', None)
    session.pop('email', None)
    session.pop('first_name', None)
    return redirect(url_for('sign_in'))


@app.route('/get_products', methods=["GET"])
def get_products():
    params = {"key" : API_KEY}
    endpoint = API_ENDPOINT + "get_items"
    response = re.post(url=endpoint, data=params)
    response = json.loads(response.text)

    if response['result'] == "success":
        products = response['items']
        return json.dumps(products)

    return ""


@app.route('/item/<int:id>', methods=["GET", "POST"])
def show_item(id):
    data = {'msg' : None,
            'item': None}

    if request.method == "POST":
        item_id = request.form["item_id"]
        price_per_item = request.form["price"]
        quantity = request.form["quantity"]

        if 'email' in session:
            email = session['email']
            
            params = {"email" : email,
                      "quantity" : quantity,
                      "price_per_item" : price_per_item,
                      "item_id" : item_id,
                      "key" : API_KEY}

            endpoint = API_ENDPOINT + "add_to_cart"
            response = re.post(url=endpoint, data=params)
            response = json.loads(response.text)

            if response["result"] == "success":
                data['msg'] = "Item added to cart"
            else:
                data['msg'] = "Error adding item to cart"

        else:
            data['msg'] = "Sign in first"


    params = {"item_id" : id,
              "key" : API_KEY}

    endpoint = API_ENDPOINT + "item_by_id"
    response = re.post(url=endpoint, data=params)
    response = json.loads(response.text)

    if response['result'] == "success":
        data['item'] = response['item']
        return render_template('item.html', data=data)

    # implement error page
    return "<html>Item not found</html>"


@app.route('/cart')
def cart():
    data = {'msg' : None,
            'cart': None}

    if 'logged_in' in session and 'email' in session:
        email = session['email']

        params = {"email" : email,
                    "key" : API_KEY}

        endpoint = API_ENDPOINT + "cart"
        response = re.post(url=endpoint, data=params)
        response = json.loads(response.text)

        if response['result'] == "success":
            data['cart'] = response['cart']
        elif response['result'] == "empty":
            data['msg'] = "Your cart is empty"
        else:
            data['msg'] = "Error viewing cart"
        
    else:
        data['msg'] = "Sign in to see your cart"

    return render_template('cart.html', data=data)


@app.route('/account')
def account():
    data = {'msg' : None,
            'first_name' : None,
            'last_name' : None}

    if 'logged_in' in session:
        if session['logged_in']:
            params = {"email" : session['email'],
                    "key" : API_KEY}

            endpoint = API_ENDPOINT + "account"
            response = re.post(url=endpoint, data=params)
            response = json.loads(response.text)

            if response['result'] == "success":
                data['first_name'] = response['first_name']
                data['last_name'] = response['last_name']
    else:
        data['msg'] = "Sign in to see your account details"

    return render_template('account.html', data=data)


@app.route('/delete_account')
def delete_account():
    if 'logged_in' in session:
        if session['logged_in']:
            params = {"email" : session['email'],
                      "key" : API_KEY}

            endpoint = API_ENDPOINT + "delete_account"
            response = re.post(url=endpoint, data=params)
            response = json.loads(response.text)

            session.pop('logged_in', None)
            session.pop('email', None)
            session.pop('first_name', None)
    
            return redirect(url_for('home'))


@app.route('/change_name', methods=["POST"])
def change_name():
    data = {'msg' : None}

    if request.method == "POST":
        email = session['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        params = {"email" : email,
                  "first_name" : first_name.title(),
                  "last_name" : last_name.title(),
                  "key" : API_KEY}

        # change first name stored in session
        if len(first_name):
            session['first_name'] = first_name

        endpoint = API_ENDPOINT + "change_name"
        response = re.post(url=endpoint, data=params)
        response = response.json()

        if response['result'] == "success":
            data['msg'] = "Changed name successfully!"
        else:
            data['msg'] = "Error changing name."

        return redirect(url_for('account'))


@app.route('/change_password', methods=["POST"])
def change_password():
    data = {'msg' : None}

    if request.method == "POST":
        email = session['email']
        password = request.form['password']

        params = {"email" : email,
                  "password" : password,
                  "key" : API_KEY}

        endpoint = API_ENDPOINT + "change_password"
        response = re.post(url=endpoint, data=params)
        response = response.json()

        if response['result'] == "success":
            data['msg'] = "Changed password successfully!"
        else:
            data['msg'] = "Error changing password."

        return redirect(url_for('account'))


@app.route('/checkout', methods=["POST", "GET"])
def checkout():
    data = {'msg': None,
            'cart_data' : None}

    if 'logged_in' in session and 'email' in session:
        email = session['email']

        # get cart items
        params = {"email" : email,
                  "key" : API_KEY}

        endpoint = API_ENDPOINT + "cart"
        response = re.post(url=endpoint, data=params)
        response = json.loads(response.text)

        if response['result'] == "success":
            # calculate order total
            cart_total = 0.0

            for item in response['cart']:
                cart_total = cart_total + (item['price'] * item['quantity'])

            data['cart_data'] = {}
            data['cart_data']['cart'] = response['cart']
            data['cart_data']['cart_total'] = cart_total

            empty_fields = False

            # check for empty fields only, apt_no(address line 2) can be empty
            if request.method == "POST":
                for key, value in request.form.items():
                    if len(value) == 0 and key != 'apt_no':
                        data['msg'] = "Only Apt no can be empty!"
                        empty_fields = True

                if not empty_fields:
                    # name on the address
                    name = request.form['name']
                    # contact for the order
                    phone = request.form['phone']

                    address = {}
                    # address line 1
                    address["street"] = request.form['street']
                    # address line 2
                    address["apt_no"] = request.form['apt_no']
                    # city
                    address["city"] = request.form['city']
                    # state
                    address["state"] = request.form['state']
                    # zip code
                    address["zip_code"] = request.form['zip_code']
                    # country
                    address['country'] = request.form['country']

                    params = {"email" : email,
                            "name" : name,
                            "phone" : phone,
                            "address" : address,
                            "total_amount" : data['cart_data']['cart_total'],
                            "key" : API_KEY}

                    endpoint = API_ENDPOINT + "checkout"
                    response = re.post(url=endpoint, json=params)

                    try:
                        response = response.json()
                        if response['result'] == "success":
                            data['msg'] = "Order successful!"
                            data['cart_data'] = None
                        else:
                            data['msg'] = "Your order could not be placed."
                    except:
                        data['msg'] = "Your order could not be placed."

        elif response['result'] == "empty":
            data['msg'] = "Your cart is empty."

        return render_template('checkout.html', data=data)

    # if user is not signed in
    return redirect(url_for(sign_in))


if __name__ == "__main__":
    app.run(debug=True, port=5000)