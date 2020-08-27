"""Test views with no user"""

# to run test:
#     FLASK_ENV=production py -m unittest tests/test_views_no_user.py

# import os
from unittest import TestCase, mock

from models import db
from tests.openstate_info_mock import latLng, all_info

# os.environ['DATABASE_URL'] = "postgresql:///ask_your_rep_test"

from app import app, CURR_USER_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ask_your_rep_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

class ViewsTestCaseNoUser(TestCase):

    def setUp(self):
        """Make sure we start with a clean slate"""

        db.drop_all()
        db.create_all()
    
    def tearDown(self):

        resp = super().tearDown()
        db.session.rollback()

        return resp

    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', html)
            self.assertIn('Signup', html)
            self.assertNotIn('My Interactions', html)
            self.assertNotIn('Logout', html)

    #this doesn't seem to be working
    # @mock.patch('models.Representative.find_latlng', return_value=latLng)
    # @mock.patch('models.Representative.find_reps', return_value=all_info)
    # def test_your_reps(self, mock_find_latlng, mock_find_reps):
    #     with app.test_client() as client:
    #         d = {'address': '1313 Mockingbird Ln.'}
    #         resp = client.get("/your-reps", data= d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('Login', html)
    #         self.assertIn('Signup', html)
    #         self.assertIn('Signup and keep track of your communications with your representatives.', html)
    #         self.assertNotIn('My Interactions', html)
    #         self.assertNotIn('Logout', html)
    
    def test_user(self):
        with app.test_client() as client:
            resp = client.get("/user", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', html)
            self.assertIn('Signup', html)
            self.assertIn('Signup and keep track of your communications with your representatives.', html)
            self.assertNotIn('My Interactions', html)
            self.assertNotIn('Logout', html)
    
    def test_user_edit(self):
        with app.test_client() as client:
            resp = client.get("/user/edit", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', html)
            self.assertIn('Signup', html)
            self.assertIn('Signup and keep track of your communications with your representatives.', html)
            self.assertNotIn('My Interactions', html)
            self.assertNotIn('Logout', html)
    
    def test_user_interactions(self):
        with app.test_client() as client:
            resp = client.get("/user/interactions", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', html)
            self.assertIn('Signup', html)
            self.assertIn('Signup and keep track of your communications with your representatives.', html)
            self.assertNotIn('My Interactions', html)
            self.assertNotIn('Logout', html)
    
    def test_user_interactions_add(self):
        with app.test_client() as client:
            resp = client.get("/user/interactions/add", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', html)
            self.assertIn('Signup', html)
            self.assertIn('Signup and keep track of your communications with your representatives.', html)
            self.assertNotIn('My Interactions', html)
            self.assertNotIn('Logout', html)
    
    def test_user_interactions_edit(self):
        with app.test_client() as client:
            resp = client.get("/user/interaction/1/edit", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', html)
            self.assertIn('Signup', html)
            self.assertIn('Signup and keep track of your communications with your representatives.', html)
            self.assertNotIn('My Interactions', html)
            self.assertNotIn('Logout', html)


