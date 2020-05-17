import unittest

from app.models.usuario import Usuario
from tests.base import BaseTestCase

class SesionResourceTestCase(BaseTestCase):
    def test_inicio_de_sesion_exitoso(self):
        usuario = self.crear_usuario('test@test.com', '123456')
        response, data = self.iniciar_sesion_usuario()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Usuario.validar_auth_token(data['auth_token']) == usuario.id)

    def test_inicio_de_sesion_fallido_no_registrado(self):
        response, data = self.iniciar_sesion_usuario()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['mensaje'] == 'Email o constraseña invalidos')

    def test_inicio_de_sesion_fallido_password_incorrecta(self):
        self.crear_usuario('test@test.com', '123456')
        response, data = self.post('/usuario/sesion',
                                   {
                                       'email': 'test@test.com',
                                       'password': 'otra_cosa'
                                   })
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['mensaje'] == 'Email o constraseña invalidos')

    def test_validacion_de_token_exitoso(self):
        usuario = self.crear_usuario('test@test.com', '123456')
        response, data = self.iniciar_sesion_usuario()
        response, data = self.get('/usuario/sesion',
                                  {'Authorization': f'Bearer {data["auth_token"]}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['usuario_id'], usuario.id)

    def test_validacion_de_token_fallido_token_invalido(self):
        token = 'token_invalido'
        response = self.get('/usuario/sesion',
                            {'Authorization': f'Bearer {token}'})
        self.assertEqual(response[0].status_code, 403)

    def test_validacion_de_token_fallido_token_no_enviado(self):
        response = self.get('/usuario/sesion')
        self.assertEqual(response[0].status_code, 401)

    def iniciar_sesion_usuario(self):
        return self.post('/usuario/sesion',
                         {
                             'email': 'test@test.com',
                             'password': '123456'
                         })

if __name__ == '__main__':
    unittest.main()