
import os
import unittest

from flask import current_app

import manage
import tempfile

import logging
# from app import create_app, db, User

from app import User, db

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, manage.app.config['DATABASE'] = tempfile.mkstemp()

        manage.app.logger.setLevel(logging.WARN)
        self.app = manage.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_signup(self):
        email = "charliegetzenlc@gmail.com"
        rv = self.signup(email, 'password')
        users = User.query.filter_by(email=email).all()
        self.assertEqual(len(users), 1)

    def signup(self, email, password):
        return self.app.post('/signup', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
