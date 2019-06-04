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

# flask config
app = Flask(__name__, static_folder='static')
app.secret_key = "0reiyzujsn048ri7nsaej2cpdgildcbdspdbqyee10svy6nmom"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    """ if 'logged_in' in session:
        if session['logged_in'] and len(session['email']) > 0:
            return render_template('home.html')

    return redirect(url_for("login")) """
    
    return render_template('home.html')

    
@app.route('/signup', methods=["GET", "POST"])
def user_signup():

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
def admin_signin():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Rest API endpoint
        endpoint = API_ENDPOINT + "admin_signin"

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
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid username or password. Please try again!"

    if "admin_logged_in" in session and 'email' in session:
        if session['admin_logged_in']:
            return redirect(url_for("admin_dashboard"))

    return render_template("admin_signin.html", error=error)


@app.route('/admin_dashboard')
def admin_dashboard():
    data = {}
    data['msg_type'] = None
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

                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_url)

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
                        data['msg_type'] = "success"
                    else:
                        data['msg'] = "Error adding item to stock"
                        data['msg_type'] = "error"

    return render_template('admin_dashboard.html', data=data)


@app.route('/add_item')
def add_item():
    data = {}
    data['msg_type'] = None
    data['msg'] = None

    if "admin_logged_in" in session:
        if session['admin_logged_in']:
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

                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_url)

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
                        data['msg_type'] = "success"
                    else:
                        data['msg'] = "Error adding item to stock"
                        data['msg_type'] = "error"

                return render_template('add_item.html', data=data)

        return render_template('add_item.html', data=data)
    else:
        return redirect(url_for('admin_signin'))


# work on this function !!!!1
@app.route('/edit_item', methods=["GET", "POST"])
def edit_item():
    data = None

    if "admin_logged_in" in session:
        if session['admin_logged_in']:
            if request.method == "POST":
                item_id = request.form["item_id"]
                name = request.form["name"]
                quantity = request.form["quantity"]
                tags = request.form["tags"]
                description = request.form["description"]
                price = request.form["price"]

                image_name = ""

                # save image
                if 'image' in request.files:
                    image = request.files['image']
                
                    if image.filename == "":
                        session['msg'] = "No selected file"

                    if image and allowed_file(image.filename):
                        image_name = secure_filename(image.filename)
                        image_url = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
                        image.save(image_url)

                params = {"item_id" : item_id,
                        "name" : name,
                        "quantity" : quantity,
                        "tags" : tags,
                        "description" : description,
                        "price" : price,
                        "image_url" : image_name,
                        "key" : API_KEY}

                endpoint = API_ENDPOINT + "edit_item"
                response = re.post(url=endpoint, data=params)

                if response.status_code == 200:
                    response = response.json()

                    if response['result'] == "success":
                        session['msg'] = "Saved!"
                else:
                    session['msg'] = "Server error"
                    
                return render_template('edit_item.html', data=data)
            else:
                params = {"key" : API_KEY}
                endpoint = API_ENDPOINT + "get_items"
                response = re.post(url=endpoint, data=params)
                response = json.loads(response.text)

                if response['result'] == "success":
                    products = response['items']
                    data = products
                else:
                    session['msg'] = "Error showing items"

                return render_template('edit_item.html', data=data)

    return redirect(url_for('admin_signin'))


@app.route('/delete_item', methods=["POST"])
def delete_item():
    if "admin_logged_in" in session:
        if session['admin_logged_in']:
            if request.method == "POST":
                item_id = request.form["item_id"]

                params = {"item_id" : item_id,
                          "key" : API_KEY}

                endpoint = API_ENDPOINT + "delete_item"
                response = re.post(url=endpoint, data=params)

                if response.status_code == 200:
                    response = response.json()
                    session['msg'] = "Item deleted successfully!"
                else:
                    session['msg'] = "Error deleting item"

                return redirect(url_for('edit_item'))


@app.route('/admin_signout')
def admin_signout():
    session.pop('admin_logged_in', None)
    session.pop('email', None)
    session.pop('first_name', None)
    return redirect(url_for('admin_signin'))


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
        data['msg'] = "Log in to see your cart"

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
        data['msg'] = "Log in to see your account details"

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

        print(data['msg'])
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

        print(data['msg'])
        return redirect(url_for('account'))


@app.route('/admin_account')
def admin_account():
    data = {'msg' : None,
            'first_name' : None,
            'last_name' : None}

    if 'admin_logged_in' in session:
        if session['admin_logged_in']:
            params = {"email" : session['email'],
                    "key" : API_KEY}

            endpoint = API_ENDPOINT + "admin_account"
            response = re.post(url=endpoint, data=params)
            response = json.loads(response.text)

            if response['result'] == "success":
                data['first_name'] = response['first_name']
                data['last_name'] = response['last_name']
    else:
        data['msg'] = "Log in to see your account details"

    return render_template('admin_account.html', data=data)


@app.route('/delete_admin_account')
def delete_admin_account():
    if 'admin_logged_in' in session:
        if session['admin_logged_in']:
            params = {"email" : session['email'],
                      "key" : API_KEY}

            endpoint = API_ENDPOINT + "delete_admin_account"
            response = re.post(url=endpoint, data=params)
            response = json.loads(response.text)

            session.pop('admin_logged_in', None)
            session.pop('email', None)
            session.pop('first_name', None)
    
            return redirect(url_for('home'))


@app.route('/change_admin_name', methods=["POST"])
def change_admin_name():
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

        endpoint = API_ENDPOINT + "change_admin_name"
        response = re.post(url=endpoint, data=params)
        response = response.json()

        if response['result'] == "success":
            data['msg'] = "Changed name successfully!"
        else:
            data['msg'] = "Error changing name."

        print(data['msg'])
        return redirect(url_for('admin_account'))
        

@app.route('/change_admin_password', methods=["POST"])
def change_admin_password():
    data = {'msg' : None}

    if request.method == "POST":
        email = session['email']
        password = request.form['password']

        params = {"email" : email,
                  "password" : password,
                  "key" : API_KEY}

        endpoint = API_ENDPOINT + "change_admin_password"
        response = re.post(url=endpoint, data=params)
        response = response.json()

        if response['result'] == "success":
            data['msg'] = "Changed password successfully!"
        else:
            data['msg'] = "Error changing password."

        print(data['msg'])
        return redirect(url_for('admin_account'))





# helper functions
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True)