"""District model tests"""

# to run tests:
#     py -m unittest test_district_model.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, District

# connect to the test database
os.environ['DATABASE_URL'] = "postgresql:///ask_your_rep_test"

from app import app

# create the tables for the test
db.create_all()


# app.config['WTF_CSRF_ENABLED'] = False

class DistrictModelTestCase(TestCase):

    def setUp(self):
        """ starts with a clean slate """

        db.drop_all()
        db.create_all()

        # self.client = app.test_client()

    #     self.testdistrict = District.add_district('ny', '01', 'lower')

    #     db.session.commit()

    def tearDown(self):
        """ clean it all up after testing"""
        resp = super().tearDown()
        db.session.rollback()
        
        return resp

    def test_district_add(self):
        District.add_district('ny', '01', 'lower')

        db.session.commit()

        testdistrict = District.query.get(1)
        self.assertIsNotNone(testdistrict)
        self.assertEqual(testdistrict.state, "ny")
        self.assertEqual(testdistrict.district_num, "01")
        self.assertEqual(testdistrict.house, "lower")

    def test_district_add_state_error(self):
        with self.assertRaises(exc.IntegrityError):
            District.add_district(None, '01', 'lower')

    def test_district_add_dist_num_error(self):
        # This shouldn't work
        # with self.assertRaises(TypeError):
        #     District.add_district('ny', 1, 'lower')
        with self.assertRaises(exc.IntegrityError):
            District.add_district('ny', None, 'lower')

    def test_district_add_house_error(self):
        with self.assertRaises(exc.IntegrityError):
            District.add_district('ny', '01', None)

    def test_check_district(self):
        District.add_district('ny', '01', 'lower')

        db.session.commit()

        testdistrict = District.query.get(1)
        checkeddistrict = District.check_district('ny', '01', 'lower')
        self.assertEqual(testdistrict.state, checkeddistrict.state)
        self.assertEqual(testdistrict.district_num, checkeddistrict.district_num)
        self.assertEqual(testdistrict.house, checkeddistrict.house)