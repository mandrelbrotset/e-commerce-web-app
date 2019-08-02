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

