# microservices
A platform that uses several microservices to operate.

# DOCUMENTATION
This project is divided into three parts to make use of the microservices approach.
The database, rest API and the web server.

## Setting up the database
The project is made to work with a mysql database.
Create a database in mysql, edit `config.py` to include the details needed to connect 
to the database.
Copy the commands from `create_table.sql`, paste and run it in the mysql prompt.

# MANUAL
## Accounts
There are two types of accounts, admin and user account. The user account is for the 
users of the online store, while the admin account is for managing the store.

## Admin Account
An admin account is needed to manage the store. The admin page can only be accessed 
by going to {host:port}/admin. There's a link to create an admin account from the 
{hostname}/admin page.
Admins can edit names, password as well as delete their account on the "My account" page.
"My account" page can be accessed from the dropdown button in the far right of the nav bar.

### Adding Items to the Store
Sign in as an admin, go to the admin dashboard and click on "Add Item To Stock" link.
Enter details of the item, select a picture for the item and click "Add to Stock" button.

### Editing Items Already in Stock
Sign in as an admin, go to the admin dashboard and click on "Edit Item in Stock" link.
Edit the fields and save the changes.

## User account
Users can edit names, password as well as delete their account on the "My account" page.
"My account" page can be accessed from the dropdown button in the far right of the nav bar.


## Rest-api/database.py
    |  __init__(self)
    |      Initialize self.  See help(type(self)) for accurate signature.
    |  
    |  add_address(self, address_id, address)
    |  
    |  add_admin(self, email, f_name, l_name, passw_hash, hash_salt)
    |  
    |  add_item(self, name, quantity, tags, description, price, image_url)
    |  
    |  add_to_cart(self, email, item_id, quantity)
    |  
    |  add_user(self, email, f_name, l_name, passw_hash, hash_salt)
    |  
    |  admin_details(self, email)
    |  
    |  change_admin_name(self, email, first_name, last_name)
    |      # method change name
    |  
    |  change_admin_password(self, email, password_hash, salt)
    |  
    |  change_name(self, email, first_name, last_name)
    |      # method change name
    |  
    |  change_password(self, email, password_hash, salt)
    |  
    |  check_admin(self, email)
    |  
    |  check_user(self, email)
    |  
    |  connect(self)
    |  
    | delete_admin(self, email)
    |  
    |  delete_item(self, id)
    |  
    |  delete_user(self, email)
    |  
    |  edit_item(self, item_id, name, tags, quantity, price, description, image_url)
    |  
    |   get_items(self)
    | 
    |   get_orders(self)
    |  
    |  get_user_cart(self, email)
    |  
    |  get_user_orders(self, email)
    |  
    |  in_cart(self, email, item_id)
    |  
    |  increase_quantity(self, email, item_id)
    |      # method to increase quantity of item already in Cart
    |  
    |  item_by_id(self, item_id)
    |  
    |  item_quantity(self, item_id)
    |  
    |  mark_as_fulfilled(self, id)
    |  
    |  order_items(self, order_id, email)
    |  
    |  record_order(self, order_id, email, name, phone, total_amount)
    |  
    |  user_details(self, email)
    |  
    |  validate_admin(self, email)
    |  
    |  validate_user(self, email)