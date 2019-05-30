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
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tif', 'svg'])


app = Flask(__name__, static_folder='static')
app.secret_key = "0reiyzujsn048ri7nsaej2cpdgildcbdspdbqyee10svy6nmom"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    if 'logged_in' in session:
        if session['logged_in'] and len(session['email']) > 0:
            return render_template('dashboard.html')

    return redirect(url_for("login"))

    
@app.route('/signup', methods=["GET", "POST"])
def user_signup():
    error = None

    if request.method == "POST":
        print(request.form)
        # get data from html form
        f_name = request.form["first_name"]
        l_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]

        if len(f_name) > 0 and len(l_name) > 0 and len(email) > 0 and len(password) > 8:
            # Rest API endpoint
            endpoint = API_ENDPOINT + "signup"

            # dictionary to be used as POST request data
            params = {"first_name": f_name,
                      "last_name" : l_name,
                      "email": email,
                      "password": password,
                      "key" : API_KEY}

            print(params)

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
                session.pop('admin_logged_in', None)

                return redirect(url_for("home"))
            else:
                error = [response['result']]

        else:
            error = []
            if len(f_name) <= 0:
                error.append("You must enter a first name")
            if len(l_name) <= 0:
                error.append("You must enter a last name")
            if len(email) <= 0:
                error.append("You must enter an email")
            if len(password) < 8:
                error.append("Password must length requirements")
            
    return render_template("signup.html", error=error)


@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Rest API endpoint
        endpoint = API_ENDPOINT + "login"

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

    return render_template("login.html", error=error)


@app.route('/signout')
def signout():
    session.pop('logged_in', None)
    session.pop('email', None)
    session.pop('first_name', None)
    return redirect(url_for('login'))


@app.route('/admin_signup', methods=["GET", "POST"])
def admin_signup():
    error = None
    if request.method == "POST":
        # get data from html form
        f_name = request.form["first_name"]
        l_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]

        if len(f_name) > 0 and len(l_name) > 0 and len(email) > 0 and len(password) > 8:
            # Rest API endpoint
            endpoint = API_ENDPOINT + "admin_signup"

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
                session.pop('logged_in', None)

                return redirect(url_for("admin_dashboard"))
            else:
                error = response['result']

        else:
            error = []
            if len(f_name) <= 0:
                error.append("You must enter a first name")
            if len(l_name) <= 0:
                error.append("You must enter a last name")
            if len(email) <= 0:
                error.append("You must enter an email")
            if len(password) < 8:
                error.append("Password must length requirements")
            
    return render_template("admin_signup.html", error=error)


@app.route('/admin',  methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Rest API endpoint
        endpoint = API_ENDPOINT + "admin_login"

        params = {"email" : email,
                  "password" : password,
                  "key" : API_KEY}
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
    
            session['admin_logged_in'] = True
            # redirect to dashboard

            print("Logging in")

            return redirect(url_for("admin_dashboard"))
        
        else:
            error = "Invalid username or password. Please try again!"

    if "admin_logged_in" in session:
        if session['admin_logged_in']:
            return redirect(url_for("admin_dashboard"))

    return render_template("admin_login.html", error=error)


@app.route('/admin_dashboard', methods=["GET", "POST"])
def admin_dashboard():
    data = {}
    data['msg'] = None

    if "admin_logged_in" in session:
        print("admin in session")
        if session['admin_logged_in']:
            data['email'] = session['email']
            data['first_name'] = session['first_name']

            if request.method == "POST":
                name = request.form["name"]
                quantity = request.form["quantity"]
                tags = request.form["tags"]
                description = request.form["description"]
                price = request.form["price"]
                
                if 'image' not in request.files:
                    data['msg'] = "Upload an image"

                image = request.files['image']
                
                if image.filename == "":
                    data['msg'] = "No selected file"

                image_url = ""
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(filename)

                params = {"name" : name,
                        "quantity" : quantity,
                        "tags" : tags,
                        "description" : description,
                        "price" : price,
                        "image_url" : filename,
                        "key" : API_KEY}

                endpoint = API_ENDPOINT + "add_item"
                response = re.post(url=endpoint, data=params)
                response = json.loads(response.text)

                if response["result"] == "success":
                    data['msg'] = "Item added to stock"
                else:
                    data['msg'] = "Error adding item to stock"

    return render_template('admin_dashboard.html', data=data)


@app.route('/admin_signout')
def admin_signout():
    session.pop('admin_logged_in', None)
    session.pop('email', None)
    session.pop('first_name', None)
    return redirect(url_for('admin_login'))


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
            print(response.text)
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
        data['msg'] = "Login to see your cart"

    return render_template('cart.html', data=data)


# helper functions
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True)