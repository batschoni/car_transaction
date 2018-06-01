import sqlite3

#Initialize the database for user registration
db = sqlite3.connect('registration.db')
c = db.cursor()
c.execute('''DROP TABLE registration''')
c.execute('''
    CREATE TABLE registration(id INTEGER PRIMARY KEY, first_name TEXT,
                       last_name TEXT, email TEXT, public_key TEXT unique)
''')
db.commit()
db.close()

#Initialize the database for transactions
db = sqlite3.connect('transactions.db')
c = db.cursor()
c.execute('''DROP TABLE transactions''')
c.execute('''
    CREATE TABLE transactions(id INTEGER PRIMARY KEY, vendor TEXT,
                       buyer TEXT, car TEXT unique)
''')
db.commit()
db.close()