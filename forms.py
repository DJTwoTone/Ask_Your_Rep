from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from wtforms.fields.html5 import DateField

class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), 
                                                    EqualTo('confirm', message="Your passwords must match."), 
                                                    Length(min=8, message="your password must be at least 8 characters.")])
    confirm = PasswordField("Re-eneter your password")
    
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    address = StringField("Address", validators=[InputRequired()])

class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class InteractionForm(FlaskForm):
    interaction_date = DateField('When did you interact with your representative?')
    representative = SelectField('Who did you talk to?', coerce=int)
    medium = SelectField('How did you contact your representative?', choices=[('telephone', 'telephone'), 
                                                                                ('email', 'email'),
                                                                                ('mail', 'traditional mail'),
                                                                                ('in-person', 'in-person'),
                                                                                ('telegram', 'telegram')
                                                                                ])
    topic = StringField('What was the topic of your interaction?', validators=[InputRequired()])
    content = StringField('What did you discuss?', validators=[InputRequired()])

class EditUserForm(FlaskForm):

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    address = StringField("Address", validators=[InputRequired()])

class EditInteractionForm(FlaskForm):

    interaction_date = DateField('When did you interact with your representative?', format='%m-%d-%Y')
    medium = SelectField('How did you contact your representative?', choices=[('telephone', 'telephone'), 
                                                                                ('email', 'email'),
                                                                                ('mail', 'traditional mail'),
                                                                                ('in-person', 'in-person'),
                                                                                ('telegram', 'telegram')
                                                                                ])
    topic = StringField('What was the topic of your interaction?', validators=[InputRequired()])
    content = StringField('What did you discuss?', validators=[InputRequired()])
