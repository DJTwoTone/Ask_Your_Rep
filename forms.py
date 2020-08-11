from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from wtforms.fields.html5 import DateField

class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired(message="You must enter a username")])
    password = PasswordField("Password", validators=[InputRequired(), 
                                                    EqualTo('confirm', message="Your passwords must match."), 
                                                    Length(min=8, message="your password must be at least 8 characters.")])
    confirm = PasswordField("Re-eneter your password")
    
    first_name = StringField("First Name", validators=[InputRequired(message="Please enter your first name")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Please enter your last name")])
    email = StringField("Email", validators=[InputRequired(message="Please enter your email address"), Email(message="Please enter a valid email address")])
    address = StringField("Address", validators=[InputRequired(message="We need an address to find your representatives")])

class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired(message="Please enter your username")])
    password = PasswordField("Password", validators=[InputRequired(message="Please enter your password")])

class InteractionForm(FlaskForm):
    interaction_date = DateField('When did you interact with your representative?')
    representative = SelectField('Who did you talk to?', coerce=int)
    comm_choices = [('telephone', 'telephone'), ('email', 'email'), ('mail', 'traditional mail'), ('in-person', 'in-person'), ('telegram', 'telegram')]
    medium = SelectField('How did you contact your representative?', choices=comm_choices)
    topic = StringField('What was the topic of your interaction?', validators=[InputRequired(message="Please enter the topic of your interaction")])
    content = StringField('What did you discuss?', validators=[InputRequired(message="Please enter some details of your interaction")])

class EditUserForm(FlaskForm):

    first_name = StringField("First Name", validators=[InputRequired(message="Please enter your first name")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Please enter your last name")])
    email = StringField("Email", validators=[InputRequired(message="Please enter your email address"), Email(message="Please enter a valid email address")])
    address = StringField("Address", validators=[InputRequired(message="We need an address to find your representatives")])

class EditInteractionForm(FlaskForm):

    interaction_date = DateField('When did you interact with your representative?')
    comm_choices = [('telephone', 'telephone'), ('email', 'email'), ('mail', 'traditional mail'), ('in-person', 'in-person'), ('telegram', 'telegram')]
    medium = SelectField('How did you contact your representative?', choices=comm_choices)
    topic = StringField('What was the topic of your interaction?', validators=[InputRequired(message="Please enter the topic of your interaction")])
    content = StringField('What did you discuss?', validators=[InputRequired(message="Please enter some details of your interaction")])
