"""Interactions model tests"""

# to run tests:
#     py -m unittest tests/test_interaction_model.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, Interaction, User, Representative

os.environ['DATABASE_URL'] = "postgresql:///ask_your_rep"

from app import app
from tests.openstate_info_mock import single_rep1

db.create_all()


class InteractionModelTestCase(TestCase):

    def setUp(self):
        """ starts with a clean slate"""

        db.drop_all()
        db.create_all()

        user1 = User.register('user1', '11111', 'fname1', 'lname1', 'mail1@test.com', 'test address')
        rep1 = Representative.add_rep(single_rep1)

        db.session.commit()

        user1 = User.query.get(user1.id)
        rep1 = Representative.query.get(rep1.id)

        self.user1 = user1
        self.rep1 = rep1

    def tearDown(self):
        resp =  super().tearDown()
        db.session.rollback()

        return resp

    def test_add_interaction(self):
        interaction = Interaction.add_intertaction(self.user1, self.rep1, self.rep1.district, '2020-08-26', 'email', 'stuff', 'nonsense')

        testinteraction = Interaction.query.get(1)
        self.assertIsNotNone(testinteraction)
        self.assertEqual(testinteraction.user, self.user1)
        self.assertEqual(testinteraction.representative, self.rep1)
        self.assertEqual(testinteraction.district, self.rep1.district)
        # self.assertEqual(testinteraction.interaction_date, '2020-08-26')
        self.assertEqual(testinteraction.medium, 'email')
        self.assertEqual(testinteraction.topic, 'stuff')
        self.assertEqual(testinteraction.content, 'nonsense')
        