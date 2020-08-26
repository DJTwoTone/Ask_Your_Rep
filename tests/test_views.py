"""Test views"""

# to run test:
#     FLASK_ENV=production py -m unittest tests/test_views.py

import os
from unittest import TestCase

from models import db, connect_db

os.environ['DATABASE_URL'] = "postgresql:///ask_your_rep_test"

from app import app, CURR_USER_KEY

db.create_all()

class ViewsTestCase(TestCase):

    