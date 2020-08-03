"""Models of Ask Your Rep app"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import requests

db = SQLAlchemy()
bcrypt = Bcrypt()

mapQKey = 'n2BFbDxJHnrRNG5um6e81nYoGcHGbBm7'
openStatesKey = '0c190e42-7c55-4ea7-98f4-0d9935580b33'


def connect_db(app):
    db.app = app
    db.init_app(app)


class District(db.Model):
    """Districts"""
    __tablename__ = 'districts'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    state = db.Column(db.String, nullable=False)
    district_num = db.Column(db.String, nullable=False)
    house = db.Column(db.String, nullable=False)

    @classmethod
    def check_district(cls, state, district_num, house):

        
        dist = cls.query.filter(cls.state == state,
                                 cls.district_num == district_num,
                                 cls.house == house).one_or_none()

        return dist

class Office(db.Model):
    """Representatives's offices"""
    __tablename__ = 'offices'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    representative_id = db.Column(db.Integer, db.ForeignKey('representatives.id'))

    phone = db.Column(db.String)
    address = db.Column(db.String)
    location = db.Column(db.String)

class Representative(db.Model):
    """Representatives"""
    __tablename__ = 'representatives'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'))
    district = db.relationship("District", backref='representatives')
    offices = db.relationship('Office',
                                backref='representative', cascade="all,delete")
    photo_url = db.Column(db.String)
    email = db.Column(db.String)
    serving = db.Column(db.Boolean, nullable=False)
    website = db.Column(db.String)
    party = db.Column(db.String)

    @classmethod
    def check_rep(cls, full_name, state, district_num, house, serving):
        # import pdb
        # pdb.set_trace()

        # rep = cls.query.filter(cls.full_name == full_name, 
        #                             cls.district.state == state,
        #                             cls.district.district_num == district_num,
        #                             cls.district.house == house,
        #                             cls.serving == serving).join(District).one_or_none()
        reps = cls.query.filter(cls.full_name == full_name, 
                                    cls.serving == serving).join(District).all()

        for rep in reps:
            if rep.district.state == state and rep.district.district_num == district_num and rep.district.house == house:
                return rep
        
        return []

    
    def find_reps(address):
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
        return repsResp.json()

class User(db.Model):
    """Users"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    username = db.Column(db.String, 
                        nullable=False,
                        unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    representatives = db.relationship('Representative',
                                    secondary='users_representatives')


    @classmethod
    def register(cls, username, password, first_name, last_name, email, address):
        """Sets up user with a hashed password and returns"""

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, first_name=first_name,
                    last_name=last_name, email=email,
                    address=address)

                    #need to add dosrict here

    @classmethod
    def authenticate(cls, username, password):
        """Authenticates the username and password"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    def edit_user(self, password, first_name, last_name, email, address, representatives):


        if bcrypt.check_password_hash(user.password, password):
            self


class Interaction(db.Model):
    """interactions between user and reps"""
    __tablename__ = 'interactions'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    entered_date = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow())
    interaction_date = db.Column(db.DateTime, nullable=False)
    medium = db.Column(db.String, nullable=False)
    topic = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',
                            # secondary='ints_users_reps_dists',
                            backref='interactions')
    
    rep_id = db.Column(db.Integer, db.ForeignKey('representatives.id'))
    representative = db.relationship('Representative',
                            # secondary='ints_users_reps_dists',
                            backref='interactions')
    
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'))
    district = db.relationship('District',
                            # secondary='ints_users_reps_dists',
                            backref='interactions')

class UserRepresentative(db.Model):
    """Mapping users to representatives"""
    __tablename__ = 'users_representatives'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    representive_id = db.Column(db.Integer,
                                db.ForeignKey('representatives.id'))

