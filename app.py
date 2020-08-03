from flask import Flask, render_template, redirect, request, g, session
from flask_debugtoolbar import DebugToolbarExtension
import requests

from models import db, connect_db, User, Representative, District, Office, Interaction
from forms import RegistrationForm, LoginForm, InteractionForm

CURR_USER_KEY = "curr_user"

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

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def login_user(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def logout_user():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



@app.route("/")
def home():
    """rendering the front page of the app"""
    # import pdb
    # pdb.set_trace()
    if g.user:

        return redirect("/user")

    return render_template('index.html')

@app.route("/your-reps")
def your_reps():
    address = request.args['search-input']

    reps = Representative.find_reps(address)
    return render_template('reps.html', reps=reps, address=address)

@app.route("/user")
def user_home():

    if not g.user:

        return redirect('signup')


    user = g.user
    # import pdb
    # pdb.set_trace()

    return render_template('user.html', user=user)


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
            login_user(user)
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

        user = User.register(username=username, password=password, email=email,
                            first_name=first_name, last_name=last_name, address=address)
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
            district_num = str(rep.get('district'))
            house = rep.get('chamber')
            sources = rep.get('sources')
            website = sources[0]['url']
            party = rep.get('party')

            # if not Representative.check_rep(full_name, serving):
            if not Representative.check_rep(full_name, state, district_num, house, serving):
                
                if not District.check_district(state=state, district_num=district_num, house=house):
                    dist = District(state=state, district_num=district_num, house=house)
                    db.session.add(dist)
                    db.session.commit()

                else:
                    dist = District.check_district(state=state, district_num=district_num, house=house)
                
                r = Representative(first_name=first_name,
                                    last_name=last_name,
                                    full_name=full_name,
                                    district=dist,
                                    photo_url=photo_url,
                                    email=email,
                                    serving=serving,
                                    website=website,
                                    party=party
                                    )
                db.session.add(r)
                db.session.commit()

                for office in rep['offices']:
                    o = Office(phone=office["phone"], address=office["address"], location=office["name"])

                    r.offices.append(o)
                    db.session.commit()

            else:

                r = Representative.check_rep(full_name, state, district_num, house, serving)
                
            user.representatives.append(r)
            db.session.commit()
                
            login_user(user)

        return redirect("/")

    if request.data != b'':
        address = request.args['address']
    else:
        address = ''
    form.address.data = address
    form.address.id = "search-input"
    form.address.type = "search"

    return render_template('signup.html', form=form, address=address)

@app.route("/user/interactions")
def interactions():

    return render_template('interactions.html', user=g.user)

@app.route("/user/interactions/add", methods=["GET", "POST"])
def add_interaction():

    form = InteractionForm()
    reps = [(rep.id, rep.full_name) for rep in g.user.representatives]
    repid = request.args['repId']
    form.representative.choices = reps
    form.representative.default = repid
 
    if form.validate_on_submit():

        # import pdb
        # pdb.set_trace()

        interaction_date = form.interaction_date.data
        representative = form.representative.data
        medium = form.medium.data
        topic = form.topic.data
        content = form.content.data


        #get rep
        rep = Representative.query.get(representative)
        #district
        dist = District.query.get(rep.district.id)

        interaction = Interaction(user=g.user, representative=rep, district=dist, interaction_date=interaction_date, medium=medium, topic=topic, content=content)
        db.session.add(interaction)

        db.session.commit()

        return redirect('/user/interactions')


    return render_template('add-interaction.html', form=form)

@app.route("/user/interaction/edit")
def edit_interaction():

    return


#I'm not sure I want to do this
# @app.route("/user/interaction/delete")
# def del_interaction():

#     return

@app.route("/logout")
def logout():

    logout_user()

    return redirect('/')
    