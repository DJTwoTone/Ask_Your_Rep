from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ask_your_rep_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "Give me liberty, or give me death"

debug = DebugToolbarExtension(app)

@app.route("/")
def home():

    return

@app.route("/your-reps")
def your_reps():

    return

@app.route("/user")
def user_home():

    return

@app.route("/user/redistrict")
def redistrict():

    return

@app.route("/user/edit")
def edit_user():

    return

@app.route("/login")
def login():

    return

@app.route("/signup")
def signup():

    return

@app.route("/user/interactions")
def interactions():

    return

@app.route("/user/interactions/add")
def add_interaction():

    return

@app.route("/user/interaction/edit")
def edit_interaction():

    return

@app.route("/user/interaction/delete")
def del_interaction():

    return