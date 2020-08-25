"""User model tests"""

# to run tests:

#     py -m unittest test_user_model.py

import os
# import requests
from unittest import TestCase, mock
# from mock import patch
from sqlalchemy import exc
from models import db, User, Representative

# connect to the test database

os.environ['DATABASE_URL'] = "postgresql:///ask_your_rep_test"

from app import app
from tests.openstate_info_mock import latLng, all_info

# create the tables for the test

db.create_all()

class UserModelTestCase(TestCase):
    """Tests the User model"""

    def setUp(self):
        """start with a clean slate"""

        db.drop_all()
        db.create_all()

        user1 = User.register('user1', '11111', 'fname1', 'lname1', 'mail1@test.com', 'test address')

        db.session.commit()

        user1 = User.query.get(user1.id)

        self.user1 = user1


    def tearDown(self):
        """ clean it all up after testing"""
        resp = super().tearDown()
        db.session.rollback()
        
        return resp

    def test_user_add(self):
        User.register('testuser', '12345', 'test_f_name', 'test_l_name', 'test@test.com', '1313 Mockingbird Ln.')

        testuser = User.query.get(2)
        self.assertIsNotNone(testuser)
        self.assertEqual(testuser.username, 'testuser')
        self.assertEqual(testuser.first_name, 'test_f_name')
        self.assertEqual(testuser.last_name, 'test_l_name')
        self.assertEqual(testuser.email, 'test@test.com')
        self.assertEqual(testuser.address, '1313 Mockingbird Ln.')

    def test_user_add_nousername(self):
        with self.assertRaises(exc.IntegrityError):
            User.register(None, '12345', 'test_f_name', 'test_l_name', 'test@test.com', '1313 Mockingbird Ln.')

    def test_user_add_nopassword(self):
        with self.assertRaises(ValueError):
            User.register('testuser', None , 'test_f_name', 'test_l_name', 'test@test.com', '1313 Mockingbird Ln.')
    
    def test_user_add_nofname(self):
        with self.assertRaises(exc.IntegrityError):
            User.register('testuser', '12345', None, 'test_l_name', 'test@test.com', '1313 Mockingbird Ln.')
    
    def test_user_add_nolname(self):
        with self.assertRaises(exc.IntegrityError):
            User.register('testuser', '12345', 'test_f_name', None, 'test@test.com', '1313 Mockingbird Ln.')
    
    def test_user_add_noemail(self):
        with self.assertRaises(exc.IntegrityError):
            User.register('testuser', '12345', 'test_f_name', 'test_l_name', None, '1313 Mockingbird Ln.')
    
    def test_user_add_noaddress(self):
        with self.assertRaises(exc.IntegrityError):
            User.register('testuser', '12345', 'test_f_name', 'test_l_name', 'test@test.com', None)

    def test_authentication(self):
        user = User.authenticate(self.user1.username, '11111')
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user1.id)

    def test_wrong_username(self):
        self.assertFalse(User.authenticate('notauser', '11111'))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.user1.username, 'wrongpassword'))


    @mock.patch('models.Representative.find_latlng', return_value=latLng)
    @mock.patch('models.Representative.find_reps', return_value=all_info)
    def test_edit_user_fname(self, mock_find_latlng, mock_find_reps):

        user = User.query.get(self.user1.id)
        user.edit_user('new_fname', 'lname1', 'mail1@test.com', 'test address')

        self.assertEqual(user.first_name, 'new_fname')
    
    @mock.patch('models.Representative.find_latlng', return_value=latLng)
    @mock.patch('models.Representative.find_reps', return_value=all_info)
    def test_edit_user_lname(self, mock_find_latlng, mock_find_reps):

        user = User.query.get(self.user1.id)
        user.edit_user('fname1', 'new_lname', 'mail1@test.com', 'test address')

        self.assertEqual(user.last_name, 'new_lname')
    
    @mock.patch('models.Representative.find_latlng', return_value=latLng)
    @mock.patch('models.Representative.find_reps', return_value=all_info)
    def test_edit_user_email(self, mock_find_latlng, mock_find_reps):

        user = User.query.get(self.user1.id)
        user.edit_user('fname1', 'lname1', 'newmail@test.com', 'test address')

        self.assertEqual(user.email, 'newmail@test.com')
    
    @mock.patch('models.Representative.find_latlng', return_value=latLng)
    @mock.patch('models.Representative.find_reps', return_value=all_info)
    def test_edit_user_address(self, mock_find_latlng, mock_find_reps):

        user = User.query.get(self.user1.id)
        user.edit_user('fname1', 'lname1', 'mail1@test.com', 'new address')

        self.assertEqual(user.address, 'new address')