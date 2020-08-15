"""User model tests"""

# to run tests:

#     py -m unittest test_user_model.py

import os
from betamax import Betamax
import requests
from unittest import TestCase

with Betamax.configure() as config:
    config.cassette_library_dir = 'tests/fixtures/cassettes'

from models import db

# connect to the test database

os.environ['DATABASE_URL'] = "postgresql:///ask_your_rep_test"

from app import app

# create the tables for the test

db.create_all()

class UserModelTestCase():
    """Tests the User model"""

    def setUp(self):
        """start with a clean slate"""

        db.drop_all()
        db.create_all()

    def tearDown(self):
        """ clean it all up after testing"""
        resp = super().tearDown()
        db.session.rollback()
        
        return resp

    