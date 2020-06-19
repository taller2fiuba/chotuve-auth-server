import unittest

from tests.base import BaseTestCase

class AppTestCase(BaseTestCase):
    def test_ping(self):
        response = self.app.get('/ping')
        self.assertEqual(response.json, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], '*')

if __name__ == '__main__':
    unittest.main()
