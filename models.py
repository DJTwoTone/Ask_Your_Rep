"""Models of Ask Your Rep app"""
# import pdb
# pdb.set_trace()
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

    @classmethod
    def add_district(cls, state, district_num, house):
        dist = cls(state=state, district_num=district_num, house=house)
        db.session.add(dist)
        db.session.commit()

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

    @classmethod
    def add_office(cls, office):
        return cls(phone=office["phone"], address=office["address"], location=office["name"])


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
    websites = db.Column(db.JSON)
    party = db.Column(db.String)

    @classmethod
    def check_rep(cls, full_name, state, district_num, house, serving):

        reps = cls.query.filter(cls.full_name == full_name, 
                                    cls.serving == serving).join(District).all()

        for rep in reps:
            if rep.district.state == state and rep.district.district_num == district_num and rep.district.house == house:
                return rep
        
        return []
    
    def find_latlng(address):
        geodata = requests.get('http://www.mapquestapi.com/geocoding/v1/address', 
                            params={
                                'key': mapQKey,
                                'location': address
                                    })

        jdata = geodata.json()
        latLng = jdata['results'][0]['locations'][0]['latLng']
        return latLng
        
    def find_reps(self, address):

        latLng = self.find_latlng(address)
        lat = latLng['lat']
        lng = latLng['lng']

        repsResp = requests.get('http://www.openstates.org/api/v1/legislators/geo',
                        params={
                            'apikey': openStatesKey,
                            'lat': lat,
                            'long': lng
                        })
        return repsResp.json()

    #this needs to be broken down some
    @classmethod
    def add_rep(cls, rep):
            full_name = rep.get('full_name')
            first_name=rep.get('first_name')
            last_name=rep.get('last_name')
            full_name=rep.get('full_name')
            photo_url=rep.get('photo_url')
            email=rep.get('email')
            serving=rep.get('active')
            state = rep.get('state')
            district_num = str(rep.get('district'))
            house = rep.get('chamber')
            sources = rep.get('sources')
            if sources == []:
                websites = 'None'
            else:
                websites = sources
            party = rep.get('party')
            offices = rep.get('offices')

            if not Representative.check_rep(full_name, state, district_num, house, serving):
                
                if not District.check_district(state=state, district_num=district_num, house=house):
                    dist = District.add_district(state=state, district_num=district_num, house=house)

                else:
                    dist = District.check_district(state=state, district_num=district_num, house=house)
                
                r = cls(first_name=first_name,
                                    last_name=last_name,
                                    full_name=full_name,
                                    district=dist,
                                    photo_url=photo_url,
                                    email=email,
                                    serving=serving,
                                    websites=websites,
                                    party=party
                                    )
      
                db.session.add(r)
                db.session.commit()

                for office in offices:

                    o = Office.add_office(office)

                    r.offices.append(o)
                    db.session.commit()

                return r

            else:

                return Representative.check_rep(full_name, state, district_num, house, serving)
                

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

        user = cls(username=username, password=hashed_utf8, first_name=first_name,
                    last_name=last_name, email=email,
                    address=address)
        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Authenticates the username and password"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    def edit_user(self, first_name, last_name, email, address):
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.representatives = []
        reps = Representative.find_reps(address)
        for rep in reps:
            r = Representative.add_rep(rep)
            self.representatives.append(r)

        db.session.commit()

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

    @classmethod
    def add_intertaction(cls, user, representative, district, interaction_date, medium, topic, content):
        interaction = cls(user=user, 
                            representative=representative, 
                            district=district, 
                            interaction_date=interaction_date, 
                            medium=medium, 
                            topic=topic, 
                            content=content)
        db.session.add(interaction)
        db.session.commit()
    
    def edit_interaction(self, interaction_date, medium, topic, content):
        self.interaction_date = interaction_date
        self.medium = medium
        self.topic = topic
        self.content = content

        db.session.commit()



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

