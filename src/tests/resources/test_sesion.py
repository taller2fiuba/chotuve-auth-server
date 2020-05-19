import unittest

from app.models.usuario import Usuario
from tests.base import BaseTestCase

class SesionResourceTestCase(BaseTestCase):
    def test_inicio_de_sesion_exitoso(self):
        usuario = self.crear_usuario('test@test.com', '123456')
        response = self.iniciar_sesion_usuario()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Usuario.validar_auth_token(response.json['auth_token']) == usuario.id)

    def test_inicio_de_sesion_fallido_no_registrado(self):
        response = self.iniciar_sesion_usuario()
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json['mensaje'] == 'Email o constraseña invalidos')

    def test_inicio_de_sesion_fallido_password_incorrecta(self):
        self.crear_usuario('test@test.com', '123456')
        response = self.app.post('/usuario/sesion', json={
            'email': 'test@test.com',
            'password': 'otra_cosa'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json['mensaje'] == 'Email o constraseña invalidos')

    def test_validacion_de_token_exitoso(self):
        usuario = self.crear_usuario('test@test.com', '123456')
        response = self.iniciar_sesion_usuario()
        response = self.app.get('/usuario/sesion', headers={
            'Authorization': f'Bearer {response.json["auth_token"]}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['usuario_id'], usuario.id)

    def test_validacion_de_token_fallido_token_invalido(self):
        token = 'token_invalido'
        response = self.app.get('/usuario/sesion', headers={
            'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 401)

    def test_validacion_de_token_fallido_token_no_enviado(self):
        response = self.app.get('/usuario/sesion')
        self.assertEqual(response.status_code, 401)

    def iniciar_sesion_usuario(self):
        return self.app.post('/usuario/sesion', json={
            'email': 'test@test.com',
            'password': '123456'})

if __name__ == '__main__':
    unittest.main()
