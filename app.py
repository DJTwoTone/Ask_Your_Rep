from flask import Flask, render_template, redirect, request, g
from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User, Representative, District
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ask_your_rep_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

app.config['SECRET_KEY'] = "Give me liberty, or give me death"
# mapQKey = 'n2BFbDxJHnrRNG5um6e81nYoGcHGbBm7'
# openStatesKey = '0c190e42-7c55-4ea7-98f4-0d9935580b33'

debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    """rendering the front page of the app"""

    """do something to see if user is logged in"""

    return render_template('index.html')

@app.route("/your-reps")
def your_reps():
    address = request.args['search-input']

    reps = Representative.find_reps(address)
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

    address = request.args['address']
    form = RegistrationForm()
    form.address.data = address
    form.address.id = "search-input"
    form.address.type = "search"

    # import pdb
    # pdb.set_trace()

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
        
        reps = Representative.find_reps(address)

        for rep in reps:
            full_name = rep.get('full_name')
            first_name=rep.get('first_name'),
            last_name=rep.get('last_name'),
            full_name=rep.get('full_name'),
            photo_url=rep.get('photo_url'),
            email=rep.get('email'),
            serving=rep.get('active')
            state = rep.get('state')
            district_num = rep.get('district_num')
            house = rep.get('house')

            if not Representative.check_rep(full_name, serving):
            # if not Representative.check_rep(full_name, state, district_num, house, serving):
                
                r = Representative(first_name=first_name,
                                    last_name=last_name,
                                    full_name=full_name,
                                    photo_url=photo_url,
                                    email=email,
                                    serving=serving,
                                    )
                db.session.add(r)
                db.session.commit()

                if not District.check_district(state=state, district_num=district_num, house=house):
                    dist = District(state=state, district_num=district_num, house=house)
                    db.session.add(dist)
                    db.session.commit()

                else:
                    dist = District.check_district(state=state, district_num=district_num, house=house)
                
                r.district.append(dist)
                db.session.commit()

                for office in rep.offices:
                    o = Office(phone=office.phone, address=office.address, location=office.name)

                    r.offices.append(o)
                    db.session.commit()

            else:

                r = Representative.check_rep(full_name, serving)
                # r = Representative.check_rep(full_name, state, district_num, house, serving)
                
            user.representatives.append(r)
            db.session.commit()
                
                
                
                
                
                
                
                
                
                # state = rep.get('state')
                # district_num = rep.get('district'),
                # house = rep.get('chamber')
                
                # if not District.check_district(
                #                                 state=state,
                #                                 district_num=district_num,
                #                                 house=house
                #                                 ):
                #     dist = District(state=state, district_num=district_num, house=house)
                #     session.add(dist)
                #     session.commit()
                # else:
                #     dist = District.check_district(
                #                                 state=state,
                #                                 district_num=district_num,
                #                                 house=house
                #                                 )

                # import pdb
                # pdb.set_trace()


        # return reps
        return redirect("/user", user=user)

    return render_template('signup.html', form=form, address=address)

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
    