from flask import Flask, request, render_template, flash, session, redirect, \
    url_for, send_from_directory, flash
import requests as re
from werkzeug.utils import secure_filename
import json
import config


API_ENDPOINT = config.REST_API
API_KEY = "193420702d05eb046e6690b2b4a0fc53ec6a52dee3853e568ea55d09526922cf"
UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tif', 'svg'])

# flask config
app = Flask(__name__, static_folder='static')
app.secret_key = "2cpdgildcbdspdbqyee10svy6nmom0reiyzujsn048ri7nsaej"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin_signup', methods=["GET", "POST"])
def admin_signup():
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
                session['admin_logged_in'] = True
                session['email'] = email
                # save first name in  session storage with first letter capitalized
                session['admin_first_name'] = f_name.title()
                # redirect to dashboard
                session.pop('logged_in', None)

                return redirect(url_for("admin_dashboard"))
            else:
                error = response['result']

        else:
            error = []
            if len(f_name) <= 0:
                flash("You must enter a first name")
            if len(l_name) <= 0:
                flash("You must enter a last name")
            if len(email) <= 0:
                flash("You must enter an email")
            if len(password) < 8:
                flash("Password must length requirements")
            
    return render_template("admin_signup.html")


@app.route('/',  methods=["GET", "POST"])
def admin_signin():
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
            session['admin_first_name'] = response['first_name'].title()
    
            session['admin_logged_in'] = True
            # redirect to dashboard
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid username or password. Please try again!")

    if "admin_logged_in" in session and 'email' in session:
        if session['admin_logged_in']:
            return redirect(url_for("admin_dashboard"))

    return render_template("admin_signin.html")


@app.route('/admin_dashboard')
def admin_dashboard():
    if "admin_logged_in" in session:
        if session['admin_logged_in']:
            data = {}
            data['email'] = session['email']
            data['first_name'] = session['admin_first_name']

            # get items currently in stock
            params = {"key" : API_KEY}
            endpoint = API_ENDPOINT + "get_items"
            response = re.post(url=endpoint, data=params)
            response = response.json()
            
            data['products'] = None
            if response['result'] == "success":
                data['products'] = response['items']

            # get orders
            params = {"key" : API_KEY}
            endpoint = API_ENDPOINT + "all_orders"
            response = re.post(url=endpoint, data=params)
            orders = None

            response = response.json()
            if response['fulfilled_orders'] != None and response['fulfilled_orders'] != None:
                orders = {}
                orders['fulfilled_orders'] = response['fulfilled_orders']
                orders['unfulfilled_orders'] = response['unfulfilled_orders']
            else:
                flash("An error ocurred while retrieving ordered item")

            return render_template('admin_dashboard.html', data=data, orders=orders)
    else:
        return redirect(url_for("admin_signin"))


@app.route('/item/<int:id>')
def show_item(id):
    data = {'item': None}

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


@app.route('/fulfill_order', methods=["POST"])
def fulfill_order():
    if "admin_logged_in" in session and session['admin_logged_in']:
        print("hello 1")

        if request.method == "POST":
            print("hello post")

            # save fulfilled order
            order_id = request.form["order_id"]

            print("id:", order_id)

            params = {"key" : API_KEY,
                        "order_id" : order_id}
            endpoint = API_ENDPOINT + "fulfill_order"
            response = re.post(url=endpoint, data=params)
            response = response.json()

            # show the success or failure message
            if response["result"] == "success":
                flash("Marked order as fulfilled!")
            else:
                flash("Error marking order as fulfilled")

            redirect(url_for("admin_dashboard"))

    return redirect(url_for('admin_signin'))

@app.route('/add_item', methods=["POST"])
def add_item():
    if "admin_logged_in" in session and session['admin_logged_in']:
        if request.method == "POST":
            name = request.form["name"]
            quantity = request.form["quantity"]
            tags = request.form["tags"]
            description = request.form["description"]
            price = request.form["price"]
            
            error_flag = False

            # save image
            image_url = ""
            image_url = save_image(request.files, 'image')
            if not image_url:
                error_flag = True
                flash("Upload an image")

            if len(name) < 1 or len(quantity) < 1 or len(description) < 1 or len(price) < 1:
                flash("Only tags can be empty")
                error_flag = True
            
            if not error_flag:
                params = {"name" : name,
                        "quantity" : quantity,
                        "tags" : tags,
                        "description" : description,
                        "price" : price,
                        "image_url" : image_url,
                        "key" : API_KEY}

                endpoint = API_ENDPOINT + "add_item"
                response = re.post(url=endpoint, data=params)
                response = json.loads(response.text)

                if response["result"] == "success":
                    flash("Item added to stock")
                else:
                    flash("Error adding item to stock")

        return redirect(url_for('admin_dashboard'))

    else:
        return redirect(url_for('admin_signin'))


# work on this function !!!!
@app.route('/edit_item', methods=["POST"])
def edit_item():
    if "admin_logged_in" in session and session['admin_logged_in']:
        if request.method == "POST":
            item_id = request.form["item_id"]
            name = request.form["name"]
            quantity = request.form["quantity"]
            tags = request.form["tags"]
            description = request.form["description"]
            price = request.form["price"]
            image_name = request.form["image_name"]

            # save image if an image is uploaded
            if 'image' in request.files and request.files['image'].filename != "":
                image_url = save_image(request.files['image'], 'image')

                if not image_url:
                    flash("Error selected image is not supported")
                    return redirect(url_for('admin_dashboard'))
            else:
                image_url = image_name
            
            params = {"item_id" : item_id,
                    "name" : name,
                    "quantity" : quantity,
                    "tags" : tags,
                    "description" : description,
                    "price" : price,
                    "image_url" : image_url,
                    "key" : API_KEY}

            print(params)
            endpoint = API_ENDPOINT + "edit_item"
            response = re.post(url=endpoint, data=params)

            if response.status_code == 200:
                response = response.json()

                if response['result'] == "success":
                    flash("Saved!")
            else:
                flash("Server error")
                
            return redirect(url_for('admin_dashboard'))
        
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
                    flash("Item deleted successfully!")
                else:
                    flash("Error deleting item")

                return redirect(url_for('admin_dashboard'))


@app.route('/admin_signout')
def admin_signout():
    session.pop('admin_logged_in', None)
    session.pop('email', None)
    session.pop('first_name', None)
    return redirect(url_for('admin_signin'))


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
            session['admin_first_name'] = first_name

        endpoint = API_ENDPOINT + "change_admin_name"
        response = re.post(url=endpoint, data=params)
        response = response.json()

        if response['result'] == "success":
            data['msg'] = "Changed name successfully!"
        else:
            data['msg'] = "Error changing name."

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

        return redirect(url_for('admin_account'))


# helper functions
def save_image(request_files, file_name):
    if file_name in request_files and request_files[file_name].filename != "" \
    and allowed_file(request_files[file_name].filename):
        new_filename = secure_filename(request_files[file_name].filename)
        image_url = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        request_files[file_name].save(image_url)
        return new_filename
    else:
        return None

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#if __name__ == "__main__":
#    app.run(debug=True, port=5004)
