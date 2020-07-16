import unittest

from app import app
from tests.base import BaseTestCase

class UsuarioAdminTestCase(BaseTestCase):
    def test_genera_token_correcto(self):
        email = app.config.get('ADMIN_EMAIL')
        password = app.config.get('ADMIN_CLAVE')

        response = self.app.post('/usuario/admin', json={
            'email': email,
            'password': password
        })

        self.assertEqual(200, response.status_code)
        self.assertIn('auth_token', response.json)

    def test_devuelve_401_en_email_incorrecto(self):
        email = 'email-incorrecto'
        password = app.config.get('ADMIN_CLAVE')

        response = self.app.post('/usuario/admin', json={
            'email': email,
            'password': password
        })

        self.assertEqual(401, response.status_code)
        self.assertNotIn('auth_token', response.json)

    def test_devuelve_401_en_clave_incorrecta(self):
        email = app.config.get('ADMIN_EMAIL')
        password = 'clave-incorrecta'

        response = self.app.post('/usuario/admin', json={
            'email': email,
            'password': password
        })

        self.assertEqual(401, response.status_code)
        self.assertNotIn('auth_token', response.json)

    def test_devuelve_400_si_faltan_datos(self):
        email = app.config.get('ADMIN_EMAIL')

        response = self.app.post('/usuario/admin', json={
            'email': email,
        })

        self.assertEqual(400, response.status_code)
        self.assertNotIn('auth_token', response.json)


if __name__ == '__main__':
    unittest.main()
