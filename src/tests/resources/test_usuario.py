import unittest

from tests.base import BaseTestCase

class UsuarioResourceTestCase(BaseTestCase):
    def test_registracion_exitosa(self):
        response, data = self.post('/usuario',
                                   {
                                       'email': 'test@test.com',
                                       'password': '123456'
                                   })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['auth_token'])

    def test_registracion_fallida_ya_registrado(self):
        self.crear_usuario('test@test.com', '123456')
        response, data = self.post('/usuario',
                                   {
                                       'email': 'test@test.com',
                                       'password': '123456'
                                   })
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['errores']['email'] == 'El mail ya se encuentra registrado')

if __name__ == '__main__':
    unittest.main()
