"""Representative model tests"""

# to run tests:

#     py -m unittest tests/test_representative_model.py

import os
from unittest import TestCase, mock

from sqlalchemy import exc
from models import db, Representative

# connect to the test database

os.environ['DATABASE_URL'] = "postgresql:///ask_your_rep_test"

from app import app
from tests.openstate_info_mock import all_info, single_rep1, single_rep2, latLng

# create the tables for the test

db.create_all()

class RepresentativeModelTestCase(TestCase):
    """Tests the Representative model"""

    def setUp(self):
        """start with a clean slate"""

        db.drop_all()
        db.create_all()

        rep1 = Representative.add_rep(single_rep1)

        db.session.commit()

        rep1 = Representative.query.get(rep1.id)

        self.rep1 = rep1


    def tearDown(self):
        """clean it all up after testing"""
        resp = super().tearDown()
        db.session.rollback()

        return resp

    def test_check_rep(self):
        testrep = Representative.check_rep('Joseph Giglio', 'ny', '148', 'lower', True)
        self.assertEqual(testrep, self.rep1)
    
    def test_check_rep_wrong_name(self):
        testrep = Representative.check_rep('Bob Lablaw', 'ny', '148', 'lower', True)
        self.assertEqual(testrep, [])
    
    def test_check_rep_wrong_state(self):
        testrep = Representative.check_rep('Joseph Giglio', 'fl', '148', 'lower', True)
        self.assertEqual(testrep, [])
    
    def test_check_rep_wrong_distnum(self):
        testrep = Representative.check_rep('Joseph Giglio', 'ny', '147', 'lower', True)
        self.assertEqual(testrep, [])
    
    def test_check_rep_wrong_house(self):
        testrep = Representative.check_rep('Joseph Giglio', 'ny', '148', 'upper', True)
        self.assertEqual(testrep, [])
    
    def test_check_rep_wrong_status(self):
        testrep = Representative.check_rep('Joseph Giglio', 'ny', '148', 'lower', False)
        self.assertEqual(testrep, [])

    @mock.patch('models.Representative.find_latlng', return_value=latLng)
    def test_find_latlng(self, mock_find_latlng):
        coords = Representative.find_latlng('testaddress')
        self.assertEqual(coords, latLng)

    @mock.patch('models.Representative.find_reps', return_value=all_info)
    @mock.patch('models.Representative.find_latlng', return_value=latLng)
    def test_find_reps(self, mock_find_latlng, mock_find_reps):
        reps = Representative.find_reps('testaddress')
        self.assertEqual(reps, all_info)
    
    def test_add_rep(self):
        Representative.add_rep(single_rep2)

        testrep = Representative.query.get(2)
        self.assertIsNotNone(testrep)
        self.assertEqual(testrep.full_name, 'George Borrello')
        self.assertEqual(testrep.first_name, 'George')
        self.assertEqual(testrep.last_name, 'Borrello')
        self.assertEqual(testrep.photo_url, '')
        self.assertEqual(testrep.email, 'borrello@nyassembly.gov')
        self.assertEqual(testrep.serving, True)
        self.assertEqual(testrep.party, 'Republican')
        # district info
        self.assertEqual(testrep.district.state, 'ny')
        self.assertEqual(testrep.district.district_num, '57')
        self.assertEqual(testrep.district.house, 'upper')
        # website info
        self.assertEqual(testrep.websites[0]['url'], "https://www.nysenate.gov/senators/george-m-borrello")
        # office info
        self.assertEqual(testrep.offices[0].location, 'Capitol Office')
        self.assertEqual(testrep.offices[0].phone, '518-455-3563')
        self.assertEqual(testrep.offices[0].address, '188 State Street, Legislative Office Building; Room 706; Albany, NY 12247')
        self.assertEqual(testrep.offices[1].location, 'District Office')
        self.assertEqual(testrep.offices[1].phone, '716-664-4603')
        self.assertEqual(testrep.offices[1].address, '2-6 E. Second Street; Fenton Building, Suite 302; Jamestown, NY 14701')
        

