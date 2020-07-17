from flask import Flask, render_template, redirect, request, g
from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ask_your_rep_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

app.config['SECRET_KEY'] = "Give me liberty, or give me death"
mapQKey = 'n2BFbDxJHnrRNG5um6e81nYoGcHGbBm7'
openStatesKey = '0c190e42-7c55-4ea7-98f4-0d9935580b33'

debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    """rendering the front page of the app"""

    """do something to see if user is logged in"""

    return render_template('index.html')

@app.route("/your-reps")
def your_reps():
    address = request.args['search-input']
    geodata = requests.get('http://www.mapquestapi.com/geocoding/v1/address', 
                            params={
                                'key': mapQKey,
                                'location': address
                                    })

    jdata = geodata.json()
    latLng = jdata['results'][0]['locations'][0]['latLng']
    lat = latLng['lat']
    lng = latLng['lng']

    repsResp = requests.get('http://www.openstates.org/api/v1/legislators/geo',
                        params={
                            'apikey': openStatesKey,
                            'lat': lat,
                            'long': lng
                        })
    reps = repsResp.json()
    return render_template('reps.html', reps=reps, address=address)

@app.route("/user")
def user_home():

    return render_template('user.html')

""""Possibly unneeded"""
# @app.route("/user/redistrict")
# def redistrict():

#     return

@app.route("/user/edit")
def edit_user():

    return render_template('edit-user.html')

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.id
            return redirect("/user")
        else:
            #refactor this to both
            form.username.errors = ["There's a problem with your username or password."]

    return render_template('login.html', form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        address = form.address.data

        user = User.register(username, password, email,
                            first_name, last_name, address)
        
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id

        return redirect("/user")

    return render_template('signup.html', form=form)

@app.route("/user/interactions")
def interactions():

    return render_template('interactions.html')

@app.route("/user/interactions/add")
def add_interaction():

    return

@app.route("/user/interaction/edit")
def edit_interaction():

    return

@app.route("/user/interaction/delete")
def del_interaction():

    return