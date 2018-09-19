# !/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from flask import current_app
from app import create_app


class BasicTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):

        app = create_app('testing')

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

        from database import db
        db.drop_all()
        db.create_all()

    def test_app_in_testing(self):
        self.assertFalse(current_app is None)
        self.assertFalse(current_app.config['SECRET_KEY' is 'asdfg'])


if __name__ == '__main__':
    unittest.main()
