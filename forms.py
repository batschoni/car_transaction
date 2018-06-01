from sql import db, all_usernames, check_id, previous_hash, all_owners
from wtforms import Form, StringField, TextAreaField, validators, ValidationError


# Definition of the form for new user registrations   
class RegistrationForm(Form):
    first_name = StringField('First Name', validators=[validators.input_required(message = "Please provide your first name")])
    last_name  = StringField('Last Name', validators=[validators.input_required(message = "Please provide your last name")])
    email  = StringField('E-Mail', validators=[validators.Email(message ='Not a valid email address')])
    public_key = StringField('Username', validators=[
            validators.input_required(message = "Please create a username"), 
            validators.Length(min=8, max=50, message = "username must be at least 8 and maximal 50 characters"),
            validators.NoneOf(all_usernames(), message="Username already exists")
            ])


# Definition of the form which is used for transaction orders    
class TransactionForm(Form):
    vendor = StringField("Vendor", validators=[
            # Checks if the input vendor id really exisits in the db
            validators.AnyOf(
                    all_usernames(),
                    message="No such Vendor exists in our database"),
            # Checks if there is an input
                    validators.InputRequired(message="Please provide the vendor ID")
            ])
    buyer = StringField("Buyer", validators=[
            # Checks if the input buyer id really exisits in the db
            validators.AnyOf(
                    all_usernames(),
                    message="No such Buyer exists in our database"),
            # Checks if there is an input        
            validators.InputRequired(message="Please provide the buyer ID")
            ])
    car = StringField("Car-ID" , validators=[
            # Checks if the input car id really exisits in the db
            validators.AnyOf(
                    all_owners().keys(),
                    message="No such Cad ID exists in our database"),
            # Checks if there is an input
            validators.InputRequired(message="Please provide the car ID")
            ])
    private_key = StringField("Secret Key")