from flask import Flask, render_template, flash, redirect, url_for, request, session
from wtforms import Form, StringField, TextAreaField, validators, ValidationError
import hashlib as hasher
import datetime as date
from blockchain import block, create_genesis_block, next_block
import numpy as np
import uuid
import requests
from sql import db, all_usernames, check_id, previous_hash, all_owners, all_loggins, get_user
from forms import RegistrationForm ,TransactionForm
from string import Template
app = Flask(__name__)

#Set Server in debug mode (no restart needed if code changed)
app.debug = True

# Definition of the home window
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/<your_car_id>', methods = ["GET", "POST"])
def car_id(your_car_id):
    # Checks whether the car id provided in the URL exists in the db
    if your_car_id not in all_owners().keys():
        # Returns an Error message if not
        return render_template('qr_error.html', your_car_id=your_car_id)  
    if request.method == "POST":
        # Calls the public key of the owner of the car id given in the URL
        owner = all_owners()[your_car_id]
        # Calls the hashed private key of the corresponding public key
        key_owner = all_loggins()[owner] 
        # Hashes the private key typed in on the website
        password = hasher.sha1(request.form["password"].encode('utf-8')).hexdigest()
        # Calls the Data of the owner
        user_data = get_user(owner)
        first_name = user_data.first_name()
        last_name = user_data.last_name()
        email = user_data.email()
        # Compares if the hashed password provided on the website and in the db match
        # It also grant access if the code "123" is typed in. This is the police code!
        if password == key_owner or password == "40bd001563085fc35165329ea1ff5c5ecbdbbeef":
            return render_template('dashboard.html', first_name = first_name,
                                   last_name = last_name, email = email,
                                   car_id = your_car_id)
        else:
            error_title = "Wrong Password!"
            error_msg = "Your password does not match with the car " + your_car_id + " Please check again. Otherwise, contact the traffic office of your canton"
            return render_template('your_car.html', error_title = error_title, error_msg = error_msg)
    return render_template('your_car.html')

# Registration page
@app.route('/register', methods = ["GET", "POST"])
def registration():
    # Assigns to the previously defined form class
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        # Creat a random secret key with two hash functions / We take only 8 characters of the hash code
        secret_key = hasher.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest()[4:12]
        # Hashes the secret key / the hashed form will be safed in the db
        secret_key_hash = hasher.sha1(secret_key.encode('utf-8')).hexdigest()
        row_id = check_id() + 1
        # Defines the hash of this block
        hash_block = block(row_id, [form.public_key.data, secret_key_hash], previous_hash()).hash
        # Defines the data which is stored in the db
        data = db(row_id ,0, 0, 0, 0, form.public_key.data, secret_key_hash, hash_block, form.first_name.data, form.last_name.data, form.email.data)
        data.user_db()
        flash("Your are now enregistered. You will receive your secret key per postal mail (for simplicity we show the secret key here: " + secret_key + ")", "success")
        return redirect(url_for('registration'))
    return render_template('register.html', form = form)


#By default, the rout function uses a get request
#However, since this site contains a form, a POST-request must be defined   
@app.route('/transaction', methods = ["GET", "POST"])
def transaction():
    #Assigns to the previously defined form class
    form = TransactionForm(request.form)
    # Takes the hashed value of the provided private key
    if request.method == "POST" and form.validate():
        private_key_hash = hasher.sha1(form.private_key.data.encode('utf-8')).hexdigest()
        # checks whether the owner of the car and the vendor matches
        if all_owners()[form.car.data] != form.vendor.data:
            flash("You are not owning a car with this ID. A transaction is therefore not possible", "danger")
        # Checks whether the hasehd private key in the db and the provided private key match
        if all_loggins()[form.vendor.data] != private_key_hash:
            flash("The secret key you typed in does not match with your profil", "danger")
        else:
            next_id = check_id() + 1
            hash_block = block(next_id, [form.vendor.data, form.buyer.data, form.car.data, form.private_key.data], previous_hash()).hash
            data = db(next_id ,form.vendor.data, form.buyer.data, form.car.data, private_key_hash, 0, 0, hash_block, 0, 0, 0)
            data.trans_db()
    return render_template('transaction.html', form = form)


# Login for the traffc office employees
@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        # Calls the password typed in
        password = hasher.sha1(request.form["password"].encode('utf-8')).hexdigest()
        if password == "388556433b2e19def6923cafa9b81c33d4074dd3":
           session["logged_in"] = True 
           flash("You are now logged in", "success")
           return redirect(url_for('registration'))
        else:
            error_title = "Wrong Password!"
            error_msg = "Your password is not correct. Please check again."
            return render_template('login.html', error_title = error_title, error_msg = error_msg)
    return render_template('login.html')


# Logout for the traffc office employees
@app.route('/logout', methods = ["GET"])
def logout():
    session["logged_in"] = False
    session.clear
    flash("You are now logged out", "success")
    return redirect(url_for('login'))

#@app.route('/newcar', methods = ["GET", "Post"])
    
if __name__ == "__main__":
    app.secret_key="123abc123"
    app.run()
    #host='0.0.0.0'