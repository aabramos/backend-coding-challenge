# !/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from app import app
from flask_testing import TestCase
from app.tasks import send_request
from config import TestConfig


class TestCelery(TestCase):
    """
        Run this test with celery worker running.
    """
    SQLALCHEMY_DATABASE_URI = TestConfig.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = TestConfig.SQLALCHEMY_TRACK_MODIFICATIONS
    TESTING = TestConfig.DEBUG
    DEBUG = TestConfig.DEBUG
    CELERY_ALWAYS_EAGER = TestConfig.CELERY_ALWAYS_EAGER

    def create_app(self):
        return app

    def setUp(self):
        self.task = send_request.apply_async(args=['Test translation', 'en', 'es'])
        self.results = self.task.get()

    def test_send_request(self):
        self.assertEqual(self.task.state, 'SUCCESS')

    def test_translation(self):
        self.assertEqual(self.results, 'Test translation')


if __name__ == '__main__':
    unittest.main()
