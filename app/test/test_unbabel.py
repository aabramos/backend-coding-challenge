# !/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from app import app
from flask_testing import TestCase
from unbabel.api import UnbabelApi
from config import TestConfig


class TestUnbabel(TestCase):
    SQLALCHEMY_DATABASE_URI = TestConfig.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = TestConfig.SQLALCHEMY_TRACK_MODIFICATIONS
    TESTING = TestConfig.DEBUG
    DEBUG = TestConfig.DEBUG

    def create_app(self):
        return app

    def test_unbabelAPI(self):
        api = UnbabelApi(
            username=TestConfig.UNBABEL_SANDBOX_USERNAME,
            api_key=TestConfig.UNBABEL_SANDBOX_KEY,
            sandbox=True,
        )
        response = api.post_translations(
            text='Test translation',
            target_language='es',
            source_language='en',
        )
        # Testing response fields
        self.assertEqual(response.status, 'new')
        self.assertTrue(response.uid)
        self.assertEqual(response.target_language, 'es')
        self.assertEqual(response.source_language, 'en')

        # Testing unused fields consistency
        self.assertIsNone(response.translation)
        self.assertIsNone(response.client)
        self.assertIsNone(response.balance)
        self.assertIsNone(response.order_number)
        self.assertIsNone(response.origin)
        self.assertIsNone(response.price_plan)
        self.assertIsNone(response.topics)
        self.assertTrue(response.price)
        self.assertEqual(response.translators, [])
        # Testing formats
        self.assertEqual(response.text_format, 'text')
        self.assertIn('Test translation', response.text)


if __name__ == '__main__':
    unittest.main()
