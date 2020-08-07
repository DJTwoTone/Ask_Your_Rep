"""District model tests"""

# to run tests:

#     py -m unittest test_district_model.py

import os
from unittest import TestCase

from models import db

# connect to the test database

os.environ['DATABASE_URL'] = "postgresql:///ask_your_rep_test"

from app import app

# create the tables for the test

db.create_all()

class DistrictModelTestCase(TestCase):
    