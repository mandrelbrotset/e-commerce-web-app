import pymysql
import config

class Database(object):
    def __init__(self):
        self.db_username = config.db_username
        self.db_host = config.db_endpoint
        self.db_name = config.db_name
        self.db_password = config.db_password        
        self.connection = None
        

    def connect(self):
        try:
            self.connection = pymysql.connect(host=self.db_host, user=self.db_username, db=self.db_name, password=self.db_password)
            self.cursor = self.connection.cursor()
            return True
        except:
            return False
            

    def add_user(self, email, f_name, l_name, passw_hash, hash_salt):
        if self.connect():
            query = """INSERT INTO Login(email, first_name, last_name, password, hash_salt) VALUES
                        ('{}', '{}', '{}', '{}', '{}')""".format(email, f_name, l_name, passw_hash, hash_salt)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True
        
        return False


    def validate_user(self, email):
        if self.connect():
            query = """SELECT password, hash_salt, first_name, last_name FROM Login 
                        WHERE email='{}'""".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        
        return None

    
    def check_user(self, email):
        if self.connect():
            query = "SELECT * FROM Login WHERE email='{}'".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            # email is available
            if result == None:
                return True
            # username is taken(not available)
            else:
                return False
        
        return None

    
    def add_admin(self, email, f_name, l_name, passw_hash, hash_salt):
        if self.connect():
            query = """INSERT INTO Admin(email, first_name, last_name, password, hash_salt) VALUES
                        ('{}', '{}', '{}', '{}', '{}')""".format(email, f_name, l_name, passw_hash, hash_salt)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True
        
        return False


    def validate_admin(self, email):
        if self.connect():
            query = """SELECT password, hash_salt, first_name, last_name FROM Admin 
                        WHERE email='{}'""".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        return None


    def check_admin(self, email):
        if self.connect():
            query = "SELECT * FROM Admin WHERE email='{}'".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            # email is available
            if result == None:
                return True
            # username is taken(not available)
            else:
                return False
        
        return None


    def add_item(self, name, quantity, tags, description, price, image_url):
        if self.connect():
            query = """INSERT INTO Item(name, quantity, tags, description, price, image_url) VALUES
                        ('{}', {}, '{}', '{}', {}, '{}')""".format(name, quantity, tags, description, price, image_url)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True

        return False


    def get_items(self):
        if self.connect():
            query = "SELECT * FROM Item"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.connection.close()

            # return all Items
            if result:
                return result
        
        return None


    def item_by_id(self, item_id):
        if self.connect():
            query = "SELECT * FROM Item WHERE id={}".format(item_id)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            # return all Items
            if result:
                return result
        
        return None


    def item_quantity(self, item_id):
        if self.connect():
            query = "SELECT quantity FROM Item WHERE id='{}'".format(item_id)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            if result:
                return result[0]
            else:
                return 0
        
        return None


    def add_to_cart(self, email, item_id, quantity):
        if self.connect():
            query = """INSERT INTO Cart(email, item_id, quantity) 
                       VALUES('{}', {}, {})""".format(email, item_id, quantity)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True

        return False


    def in_cart(self, email, item_id):
        if self.connect():
            query = "SELECT * FROM Cart WHERE email='{}' AND item_id={}".format(email, item_id)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            if result == None:
                return False
            else:
                return True
        
        return None


    def get_user_cart(self, email):
        if self.connect():
            query = "SELECT item_id, quantity FROM Cart WHERE email='{}'".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.connection.close()

            if result != None:
                return result

        return None


    # method to increase quantity of item already in Cart
    def increase_quantity(self, email, item_id):
        if self.connect():
            query = """UPDATE Cart SET quantity=quantity + 1  
                       WHERE email='{}' AND item_id={}""".format(email, item_id)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True
        
        return False


    def user_details(self, email):
        if self.connect():
            query = "SELECT first_name, last_name FROM Login WHERE email='{}'".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            return result
        
        return None


    # method change name
    def change_name(self, email, first_name, last_name):
        query = ""

        if len(first_name) > 0 and len(last_name) == 0:
            query = """UPDATE Login SET first_name='{}'
                WHERE email='{}'""".format(first_name, email)
        elif len(first_name) == 0 and len(last_name) > 0:
            query = """UPDATE Login SET last_name='{}' 
                WHERE email='{}'""".format(last_name, email)
        elif len(first_name) > 0 and len(last_name) > 0:
            query = """UPDATE Login SET first_name='{}', last_name='{}' WHERE email='{}'""" \
                .format(first_name, last_name, email)
        
        if len(query) > 0 and self.connect():
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True

        return False


    def change_password(self, email, password_hash, salt):
        if self.connect():
            query = """UPDATE Login SET password='{}', hash_salt='{}' WHERE email='{}'""" \
                .format(password_hash, salt, email)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True

        return False


    def delete_user(self, email):
        if self.connect():
            query = "DELETE FROM Login WHERE email='{}'".format(email)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True
        
        return False


    def admin_details(self, email):
        if self.connect():
            query = "SELECT first_name, last_name FROM Admin WHERE email='{}'".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            return result
        
        return None


    # method change name
    def change_admin_name(self, email, first_name, last_name):
        query = ""

        if len(first_name) > 0 and len(last_name) == 0:
            query = """UPDATE Admin SET first_name='{}'
                WHERE email='{}'""".format(first_name, email)
        elif len(first_name) == 0 and len(last_name) > 0:
            query = """UPDATE Admin SET last_name='{}' 
                WHERE email='{}'""".format(last_name, email)
        elif len(first_name) > 0 and len(last_name) > 0:
            query = """UPDATE Admin SET first_name='{}', last_name='{}' WHERE email='{}'""" \
                .format(first_name, last_name, email)
        
        if len(query) > 0 and self.connect():
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True

        return False


    def change_admin_password(self, email, password_hash, salt):
        if self.connect():
            query = """UPDATE Admin SET password='{}', hash_salt='{}' WHERE email='{}'""" \
                .format(password_hash, salt, email)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True

        return False


    def delete_admin(self, email):
        if self.connect():
            query = "DELETE FROM Admin WHERE email='{}'".format(email)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True
        
        return False


    def delete_item(self, id):
        if self.connect():
            query = "DELETE FROM Item WHERE id='{}'".format(id)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True
        
        return False


    def edit_item(self, item_id, name, tags, quantity, price, description, image_url):
        if self.connect():
            query = """UPDATE Item SET name='{}', tags='{}', quantity='{}', price='{}',
                       description='{}', image_url='{}' WHERE id={}""".format(name, 
                       tags, quantity, price, description, image_url, item_id)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            
            return True
        
        return False


    def add_address(self, address_id, address):
        if self.connect():
            query = """INSERT INTO Address(address_id, street, apt_no, city, state, zip_code, country)
                    VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".\
                    format(address_id, address['street'], address['apt_no'], address['city'],
                     address['state'], address['zip_code'], address['country'])

            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()

            return True

        return False

    def order_items(self, order_id, email):
        if self.connect():
            # get items currently in the users cart, use email as condition
            query = """SELECT i.name, i.price, c.quantity, c.item_id 
                        FROM Cart c 
                        JOIN Item i 
                            ON c.item_id = i.id 
                        WHERE email='{}'""".format(email)
            self.cursor.execute(query)
            items = self.cursor.fetchall()

            # move cart items to OrderItems
            query = "INSERT INTO OrderItem(order_id, name, price, quantity, item_id) VALUES"

            no_of_items = len(items)
            for i in range(no_of_items):
                query += ("('{}', '{}', {}, {}, {})".format(order_id, items[i][0], \
                                                float(items[i][1]), items[i][2], items[i][3]))
                if i + 1 < no_of_items:
                    query += (", ")
            self.cursor.execute(query)

            # delete items in the cart that have just been ordered
            query = "DELETE FROM Cart WHERE email='{}'".format(email)
            self.cursor.execute(query)

            self.connection.commit()
            self.connection.close()

            return True

        return False

    def record_order(self, order_id, email, name, phone, total_amount):
        if self.connect():
            query = """INSERT INTO OrderDetail(order_id, email, name, phone, total_amount, date)
                    VALUES('{}', '{}', '{}', '{}', '{}',  now())""".format(order_id, email, \
                    name, phone, total_amount)

            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()

            return True

        return False

    def get_orders(self):
        if self.connect():
            query = """SELECT o.order_id, o.name, o.email, o.phone, o.total_amount, o.date, 
                    o.fulfilled, o.fulfillment_date,
                    a.street, a.apt_no, a.city, a.state, a.zip_code, a.country 
                    FROM OrderDetail o 
                    JOIN Address a 
                    ON o.order_id = a.address_id"""

            self.cursor.execute(query)
            result = self.cursor.fetchall()

            self.connection.close()

            if result != None:
                return result

        return False
