import unittest

from tests.base import BaseTestCase

class AppTestCase(BaseTestCase):
    def test_root_text(self):
        response = self.app.get('/ping')
        self.assertEqual(response.json, {})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
