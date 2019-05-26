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
            print("Couldn't connect to database")
            return False
            
    def add_user(self, email, username, passw_hash, hash_salt):
        if self.connect():
            query = """INSERT IGNORE INTO Login(email, username, password, hash_salt) VALUES
                        ('{}', '{}', '{}', '{}')""".format(email, username, passw_hash, hash_salt)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True
        else:
            print("Connect to Database first!")
            return False

    def validate_user(self, username):
        if self.connect():
            query = "SELECT password, hash_salt FROM Login WHERE username='{}'".format(username)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        else:
            print("Connect to Database first!")
            return None

    def check_user(self, username):
        if self.connect():
            query = "SELECT * FROM Login WHERE username='{}'".format(username)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            # username is available
            if result == None:
                return True
            # username is taken(not available)
            else:
                return False
        else:
            print("Connect to Database first!")
            return None