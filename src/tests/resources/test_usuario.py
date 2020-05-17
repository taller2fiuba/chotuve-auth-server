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

    def test_get_usuario_existente(self):
        usuario = self.crear_usuario('test@test.com', '123456')
        response, data = self.get(f'/usuario/{usuario.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['email'], usuario.email)

    def test_get_usuario_inexistente(self):
        id_no_existe = 15121
        response = self.get(f'/usuario/{id_no_existe}')
        self.assertEqual(response[0].status_code, 404)

if __name__ == '__main__':
    unittest.main()
