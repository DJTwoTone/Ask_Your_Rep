"""Office model tests"""

# to run tests:
#     py -m unittest test_office_model.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, Office, Representative
from tests.openstate_info_mock import single_office, error_office, single_rep

#connect to the test databse
os.environ['DATABASE_URL'] = "postgresql:///ask_your_rep_test"

from app import app

#create the tables for the test

db.create_all()

class OfficeModelTestCase(TestCase):

    def setUp(self):
        """ starts with a clean slate"""

        db.drop_all()
        db.create_all()

    def tearDown(self):
        """ clean it all up after testing"""
        resp = super().tearDown()
        db.session.rollback()

        return resp

    def test_office_add(self):
        rep = Representative.add_rep(single_rep)
        db.session.commit()
        o = Office.add_office(single_office)
        rep.offices.append(o)
        db.session.commit()

        testoffice = Office.query.get(1)
        # import pdb
        # pdb.set_trace()
        self.assertIsNotNone(testoffice)
        self.assertEqual(testoffice.phone, '716-664-4603')
        self.assertEqual(testoffice.address, '2-6 E. Second Street; Fenton Building, Suite 302; Jamestown, NY 14701')
        self.assertEqual(testoffice.location, 'District Office')

    def test_office_add_error(self):
        with self.assertRaises(TypeError):
            Office.add_office(error_office)