import unittest

from tests.base import BaseTestCase

class UsuarioResourceTestCase(BaseTestCase):
    def test_registracion_exitosa(self):
        response = self.app.post('/usuario', json={
            'email': 'test@test.com',
            'password': '123456'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json['auth_token'])

    def test_registracion_fallida_ya_registrado(self):
        self.crear_usuario('test@test.com', '123456')
        response = self.app.post('/usuario', json={
            'email': 'test@test.com',
            'password': '123456'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json['errores']['email'] == 'El mail ya se encuentra registrado')


    def test_get_usuarios_sin_usuarios_registrados(self):
        response = self.app.get('/usuario')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(not response.json)

    def test_get_usuarios_con_usuarios_registrados(self):
        self.crear_usuario('test@test.com', '123456')
        self.crear_usuario('test2@test.com', '123456')
        self.crear_usuario('test3@test.com', '123456')

        response = self.app.get('/usuario')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)


    def test_get_usuarios_con_ids_inexistentes(self):
        self.crear_usuario('test@test.com', '123456')

        response = self.app.get('/usuario?ids=2')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(not response.json)

    def test_get_usuarios_con_ids_existentes(self):
        emails = ['a@test.com', 'b@test.com', 'c@test.com', 'd@test.com']
        for email in emails:
            self.crear_usuario(email, '123456')

        response = self.app.get('/usuario?ids=2,3')
        email_response = [usuario['email'] for usuario in response.json]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertListEqual(email_response, ['b@test.com', 'c@test.com'])

    def test_get_usuarios_con_ids_invalidos(self):
        response = self.app.get('/usuario?ids=a')
        self.assertEqual(response.status_code, 400)

    def test_get_usuarios_con_ids_repetidos(self):
        emails = ['a@test.com', 'b@test.com', 'c@test.com', 'd@test.com']
        for email in emails:
            self.crear_usuario(email, '123456')

        response = self.app.get('/usuario?ids=1,1,3,3,3')
        email_response = [usuario['email'] for usuario in response.json]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertListEqual(email_response, ['a@test.com', 'c@test.com'])


if __name__ == '__main__':
    unittest.main()
