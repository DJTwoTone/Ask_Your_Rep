"""Models of Ask Your Rep app"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    username = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    home_districts = db.relationship('District', secondary='users_districts')
    represenatives = db.relationship('Representative', secondary='users_representatives')

class UserDistrict(db.Model):
    """Mapping users to districts"""
    __tablename__ = 'users_districts'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    district_id = db.Column(db.Integer,
                            db.ForeignKey('districts.id'))

class UserRepresentative(db.Model):
    """Mapping users to representatives"""
    __tablename__ = 'users_representatives'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    representtive_id = db.Column(db.Integer,
                                db.ForeignKey('representatives.id'))

class Representative(db.Model):
    """Representatives"""
    __tablename__ = 'representatives'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    district = db.relationship('District', backref='representatives')
    photo_url = db.Column(db.String)
    email = db.Column(db.String)
    house = db.Column(db.String, nullable=False)
    serving = db.Column(db.Boolean, nullable=False)

class District(db.Model):
    """Districts"""
    __tablename__ = 'districts'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    state = db.Column(db.String, nullable=False)
    district_num = db.Column(db.Integer, nullable=False)
    house = db.Column(db.String, nullable=False)

class Office(db.Model):
    """Representatives's offices"""
    __tablename__ = 'offices'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    representative = db.relationship('Representative', backref='offices')
    phone = db.Column(db.String)
    address = db.Column(db.String)
    location = db.Column(db.String)

class Interaction(db.Model):
    """interactions between user and reps"""
    __tablename__ = 'interactions'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    user = db.relationship('User', backref='interactions')
    representative = db.relationship('Representative', backref='interactions')
    entry_date = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow())
    entered_date = db.Column(db.DateTime, nullable=False)
    medium = db.Column(db.String, nullable=False)
    topic = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
