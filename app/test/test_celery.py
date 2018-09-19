# !/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch


class TestCelery(unittest.TestCase):

    @patch('app.tasks.Translation')
    def test_success(self, send_request):
        send_request.delay('Translation test', 'en', 'es', )


if __name__ == '__main__':
    unittest.main()
