"""
Test suite for the API module.

:author: 2013, Pascal Hartig <phartig@weluse.de>
"""

import os
import json
import urllib
import mock
from unittest import TestCase
from soccerstats.application import create_app


class ApiTestCase(TestCase):
    config = {
        'TWENTIMENT_HOST': "localhost",
        'TWENTIMENT_PORT': 10001
    }

    def setUp(self):
        self.app = create_app(self.config)
        self.app.testing = True
        self.ctx = self.app.test_request_context()
        self.ctx.push()

        self.client = self.app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def read_fixture(self, filename):
        return open(os.path.join(os.path.dirname(__file__), 'fixtures',
                                 filename)).read()


class ScoreTestCase(ApiTestCase):
    def test_wikipedia_example(self):
        results = self.read_fixture('wikipedia.json')

        response = self.client.post('/v1/score', data=results)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.data)

        scores = data['scores']

        self.assertAlmostEqual(scores['Team A'], 1.625)
        self.assertAlmostEqual(scores['Team B'], 0.75)
        self.assertAlmostEqual(scores['Team C'], -0.875)
        self.assertAlmostEqual(scores['Team D'], -1.5)


class CORSTestCase(ApiTestCase):
    """Tests for some CORS stuff."""

    def setUp(self):
        config = self.config.copy()
        self.config = config

        config['CORS_ENABLED'] = True
        config['CORS_ORIGIN'] = "localhost"

        ApiTestCase.setUp(self)

    def test_preflight(self):
        response = self.client.open("/something", method='OPTIONS', headers={
            'origin': "localhost"
        })
        self.assertEqual(response.status_code, 200)

    def test_nopreflight(self):
        response = self.client.open("/something", method='OPTIONS')
        self.assertEqual(response.status_code, 404)
