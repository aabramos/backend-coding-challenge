# !/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from database import db
from app import create_app
from flask_testing import TestCase
from flask import current_app, url_for
from config import TestConfig


class BasicTests(TestCase):
    SQLALCHEMY_DATABASE_URI = TestConfig.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = TestConfig.SQLALCHEMY_TRACK_MODIFICATIONS
    TESTING = TestConfig.DEBUG
    DEBUG = TestConfig.DEBUG
    WTF_CSRF_ENABLED = TestConfig.WTF_CSRF_ENABLED

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app(self):
        self.assertFalse(current_app is None)

    def test_index(self):
        client = self.app.test_client()
        response = client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
