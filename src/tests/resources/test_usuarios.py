import unittest

from tests.base import BaseTestCase

class UsuariosResourceTestCase(BaseTestCase):
    def test_get_usuarios_sin_usuarios_registrados(self):
        response = self.app.get('/usuarios')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(not response.json)

    def test_get_usuarios_con_usuarios_registrados(self):
        self.crear_usuario('test@test.com', '123456')
        self.crear_usuario('test2@test.com', '123456')
        self.crear_usuario('test3@test.com', '123456')

        response = self.app.get('/usuarios')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)


    def test_get_usuarios_con_ids_inexistentes(self):
        self.crear_usuario('test@test.com', '123456')

        response = self.app.get('/usuarios?ids=2')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(not response.json)

    def test_get_usuarios_con_ids_existentes(self):
        emails = ['a@test.com', 'b@test.com', 'c@test.com', 'd@test.com']
        for email in emails:
            self.crear_usuario(email, '123456')

        response = self.app.get('/usuarios?ids=2,3')
        email_response = [usuario['email'] for usuario in response.json]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertListEqual(email_response, ['b@test.com', 'c@test.com'])

if __name__ == '__main__':
    unittest.main()
