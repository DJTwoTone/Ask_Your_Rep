"""Test views with a user"""

# to run test:
#     FLASK_ENV=production py -m unittest tests/test_views_with_user.py

# import os
from unittest import TestCase, mock
from flask import Flask

from models import db, User, District, UserRepresentative, Representative, Office, Interaction
from tests.openstate_info_mock import latLng, all_info

# os.environ['DATABASE_URL'] = "postgresql:///ask_your_rep_test"

from app import app, login_user

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ask_your_rep_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

class ViewsTestCasewithUser(TestCase):

    def setUp(self):
        """Make sure we start with a clean slate"""

        db.drop_all()
        db.create_all()

        Office.query.delete()
        District.query.delete() 
        Representative.query.delete()
        User.query.delete()
        Interaction.query.delete()
        UserRepresentative.query.delete()

        test_office = Office(phone='123-555-1234', address='123 Test St.', location='district')
        test_district = District(state='ny', district_num='123', house='lower')

        db.session.add(test_office)
        db.session.add(test_district)
        db.session.commit()

        office = Office.query.get(1)
        district = District.query.get(1)

        test_rep = Representative(first_name='Testy', last_name='McTestface', full_name='Testy McTestface', photo_url='https://mn315.net/wp-content/uploads/2018/06/cropped-Ugandan-Knuckles.jpg', email='test@test.test', serving=True, district=district, websites=[
                    {
                        "url": "http://www.google.com"
                    },
                    {
                        "url": "http://tesla.com"
                    }
                ])
        test_user = User.register(username='Someuser', password='1234567890', first_name='Some', last_name='User', email='some@user.com', address='123 Any St., Anytown NY 12345')
        # login_test = User.register(username='test', password='1234', first_name='test', last_name='test', email='test@test.com', address='82 Kent Blvd., Salamanca NY 14779')
        db.session.add(test_rep)
        db.session.add(test_user)
        # db.session.add(login_test)
        db.session.commit()

        user = User.query.get(1)
        self.user = user
        # user2 = User.query.get(2)
        rep = Representative.query.get(1)


        user.representatives.append(rep)
        rep.offices.append(office)
        # user2.representatives.append(rep)
        db.session.commit()

        # import pdb
        # pdb.set_trace()

        test_interaction = Interaction(user=user, representative=rep, district=district, interaction_date='2020-07-15 10:00:00', medium='email', topic='stuff and junk', content='all the things')
        db.session.add(test_interaction)

        db.session.commit()

    
    def tearDown(self):

        resp = super().tearDown()
        db.session.rollback()

        return resp

    #need to get session to work

    # def test_home(self):
    #     with app.test_client() as client:
    #         # with client.session_transaction() as sess:
    #         #     sess['CURR_USER_KEY'] = self.user.id
            
    #         print(self.user)
    #         # print(sess['CURR_USER_KEY'])

    #         resp = client.get("/", follow_redirects=True)
    #         assert Flask.session['CURR_USER_KEY'] == self.user.id
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertNotIn('Login', html)
    #         self.assertNotIn('Signup', html)
    #         self.assertIn('My Interactions', html)
    #         self.assertIn('Logout', html)
    #         self.assertIn('Someuser', html)
    #         self.assertIn('Testy McTestface', html)