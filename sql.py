from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import pymysql
import numpy as np
from wtforms import ValidationError
"""
#Connect to SQL database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql11231595:SxsfYVAL4y@sql11.freemysqlhosting.net:3306/sql11231595'
db = SQLAlchemy(app)

class database(db.Model):
    __tabelname__ = "transactions"
    id = db.Column("ID", db.Integer, primary_key=True)
    id = db.Column("Vendor", db.Unicode, primary_key=True)            
    id = db.Column("Seller", db.Unicode, primary_key=True)
    id = db.Column("Car", db.Unicode, primary_key=True)
"""

class db(object):
    
    def __init__( self, id_db, vendor, buyer, car_id, trans_p_key, public_key, private_key, hash_db, first_name, last_name, email):
        self.db = pymysql.connect(host='sql2.freesqldatabase.com', port=3306, user='sql2235559', passwd='vC7!jQ7*', db='sql2235559')
        self.c = self.db.cursor()
        self.id_db = id_db
        self.vendor = vendor
        self.buyer = buyer
        self.car_id = car_id
        self.trans_p_key = trans_p_key
        self.public_key = public_key
        self.private_key = private_key
        self.hash_db = hash_db
        self.last_name = last_name
        self.first_name = first_name
        self.email = email
    
    # Adapt the db with a new user registration    
    def user_db(self):
        try:
            #Insert a new user to the blockchain
            self.c.execute('''INSERT INTO blockchain(id_db, public_key, private_key, hash_db)
                     VALUES(%d, "%s", "%s", "%s")''' % (self.id_db, self.public_key, self.private_key, self.hash_db))
            #Insert a new user to the government's user db
            self.c.execute('''INSERT INTO users(public_key, first_name, last_name, email)
                     VALUES("%s", "%s", "%s", "%s")''' % (self.public_key, self.first_name, self.last_name, self.email))
            self.db.commit()
        except:
            # Rollback in case there is any error
            print("Connection to the db failed. Check connection!")
            self.db.rollback()
        self.db.close()
        return
    # Add a transaction to the db
    def trans_db(self):
        try:
            self.c.execute('''INSERT INTO blockchain(id_db, vendor, buyer, car_id, trans_p_key, hash_db)
                     VALUES(%d, "%s", "%s", "%s", "%s", "%s")''' % (self.id_db, self.vendor, self.buyer, self.car_id, self.trans_p_key, self.hash_db))
            self.db.commit()
        except:
            # Rollback in case there is any error
            print("Connection to the db failed. Check connection!")
            self.db.rollback()
        self.db.close()
        return

    
# Returns the highest id in the existing user db or if no data defines id = 0
def check_id():
    try:
        db = pymysql.connect(host='sql2.freesqldatabase.com', 
                             port=3306, 
                             user='sql2235559', 
                             passwd='vC7!jQ7*', 
                             db='sql2235559')
        c = db.cursor()
        c.execute('''SELECT max(id_db) FROM blockchain''')
        all_rows = c.fetchall()
        for row in all_rows:
            max_id = row[0]
        if 'id_max' in locals():
            db.close()
            return max_id
        else:
            id_max = 0
            db.close()
            return max_id
    except:
        # Rollback in case there is any error
        print("Connection to the db failed. Check connection!")
        db.rollback()
        db.close()
        return
    
# Retunrs a list with all existing usernames (public keys)    
def all_usernames():
    usernames = []
    try:
       db = pymysql.connect(host='sql2.freesqldatabase.com', 
                            port=3306, 
                            user='sql2235559', 
                            passwd='vC7!jQ7*', 
                            db='sql2235559')
       c = db.cursor()
       c.execute('''SELECT public_key FROM blockchain''')
       all_rows = c.fetchall()
       for row in all_rows:
            usernames.append(row[0])
    except:
        # Rollback in case there is any error
        print("Connection to the db failed. Check connection!")
        db.rollback()
    db.close()
    # filters out the empty elements ("") of the list
    usernames = list(filter(None, usernames))
    return usernames

def previous_hash():
    try:
       db = pymysql.connect(host='sql2.freesqldatabase.com', 
                            port=3306, 
                            user='sql2235559', 
                            passwd='vC7!jQ7*', 
                            db='sql2235559')
       c = db.cursor()
       c.execute('''SELECT hash_db FROM blockchain WHERE id_db = "%d" ''' % (check_id()))
       all_rows = c.fetchall()
       for row in all_rows:
           prev_hash = row[0]
    except:
        # Rollback in case there is any error
        print("Connection to the db failed. Check connection!")
        db.rollback()
    db.close()
    return prev_hash

# Returns a dictionnary with every car-id and the respective owner
def all_owners():
    all_rows = []
    try:
        db = pymysql.connect(host='sql2.freesqldatabase.com', 
                             port=3306, user='sql2235559', 
                             passwd='vC7!jQ7*', 
                             db='sql2235559')
        c = db.cursor()
        c.execute('''SELECT * FROM blockchain''')
        all_rows = c.fetchall()
    except:
        print("Connection to the db failed. Check connection!")
        db.rollback()
    db.close
    vendors = []
    buyers = []
    car_ids = []
    owners = {}
    for row in all_rows:
        vendors.append(row[1])
        buyers.append(row[2])
        car_ids.append(row[3])
    # Filters out every empty element ("") in the list    
    vendors = list(filter(None, vendors))
    buyers = list(filter(None, buyers))
    car_ids = list(filter(None, car_ids))
    # Assigns every buyer the car he bought
    for i in range(0, len(buyers)):
        owners[car_ids[i]] = buyers[i]
    return owners


# Returns a dictionnary with all public keys and the corresponding private keys
def all_loggins():
    all_rows = []
    try:
        db = pymysql.connect(host='sql2.freesqldatabase.com', 
                             port=3306, user='sql2235559', 
                             passwd='vC7!jQ7*', 
                             db='sql2235559')
        c = db.cursor()
        c.execute('''SELECT * FROM blockchain''')
        all_rows = c.fetchall()
    except:
        print("Connection to the db failed. Check connection!")
        db.rollback()
    db.close
    public_keys = []
    private_keys = []
    login_data = {}
    for row in all_rows:
        public_keys.append(row[5])
        private_keys.append(row[6])
    # Filters out every empty element ("") in the list    
    private_keys = list(filter(None, private_keys))
    public_keys = list(filter(None, public_keys))
    # Assigns every public key the corresponding private key
    for i in range(0, len(public_keys)):
        login_data[public_keys[i]] = private_keys[i]
    return login_data

# Returns the data of the user
class get_user:
    def __init__( self, public_key ):
        self.public_key = public_key
        try:
            db = pymysql.connect(host='sql2.freesqldatabase.com', 
                             port=3306, user='sql2235559', 
                             passwd='vC7!jQ7*', 
                             db='sql2235559')
            c = db.cursor()
            c.execute('''SELECT * FROM users''')
            all_rows = c.fetchall()
        except:
            print("Connection to the db failed. Check connection!")
            db.rollback()
        db.close
        for row in all_rows:
            if row[0] == self.public_key:
                self.data1 = row[1]
                self.data2 = row[2]
                self.data3 = row[3]
    
    def first_name(self):
            return self.data1
        
    def last_name(self):
            return self.data2
        
    def email(self):
            return self.data3
        
 
"""
data = db(2, "test", "test", "test", "test", "test", "test", "test", "test", "test", "test")
data.user_db()
data.max_id1()
data.all_usernames()
print(all_owners())
print(get_user("allmargel"))

test = get_user("allmargel")
print(test.first_name())

db = pymysql.connect(host='sql2.freesqldatabase.com', 
port=3306, user='sql2235559', 
passwd='vC7!jQ7*', 
db='sql2235559')
c = db.cursor()
c.execute('''SELECT * FROM users''')
all_rows = c.fetchall()
db.close
for row in all_rows:
    if row[0] == "allmargel":
        username = row[1]
print(username)




import qrcode
img = qrcode.make('http://127.0.0.1:5000/mercedes')
from PIL import Image
img.show()
"""