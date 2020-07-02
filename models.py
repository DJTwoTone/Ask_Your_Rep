"""Models of Ask Your Rep app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    home_district = db.relationship('District')
    represenatives = 

class Representative(db.Model):
    """Representatives"""
    __tablename__ = 'representatives'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    district = db.relationship('District')
    photo_url = db.Column(db.String)
    email = db.Column(db.String)
    serving = db.Column(db.Boolean)

class District(db.Model):
    """Districts"""
    __tablename__ = 'districts'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    state = db.Column(db.String, nullable=False)
    district_num = db.Column(db.Integer, nullable=False)

class Office(db.Model):
    """Representatives's offices"""
    __tablename__ = 'offices'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    representative
    phone = db.Column(db.String)
    address = db.Column(db.String)
    location = db.Column(db.String)

class Interaction(db.Model):
    """interactions between user and reps"""
    __tablename__ = 'interactions'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    user = db.relationship('User')
    representative = db.relationship('Representative')
    entry_date = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow())
    entered_date = db.Column(db.DateTime, nullable=False)
    medium = db.Column(db.String, nullable=False)
    topic = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
