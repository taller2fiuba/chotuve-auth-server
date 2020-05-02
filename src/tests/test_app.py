import unittest

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_root_text(self):
        response = self.app.get('/ping')
        self.assertEqual(response.json, {})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
