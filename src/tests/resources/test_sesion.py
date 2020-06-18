import unittest

from app import db
from app.models.usuario import Usuario
from tests.base import BaseTestCase

class SesionResourceTestCase(BaseTestCase):
    def test_inicio_de_sesion_exitoso(self):
        usuario = self.crear_usuario('test@test.com', '123456')
        response = self.iniciar_sesion_usuario()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Usuario.validar_auth_token(response.json['auth_token']).id, usuario.id)

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

    def test_iniciar_sesion_usuario_deshabilitado(self):
        usuario = self.crear_usuario('test@test.com', 'clave')
        usuario.habilitado = False
        db.session.commit()

        response = self.app.post('/usuario/sesion', json={
            'email': 'test@test.com',
            'password': 'clave'
        })

        self.assertEqual(response.status_code, 400)

    def test_iniciar_sesion_content_type_erroneo_devuelve_400(self):
        self.crear_usuario('test@test.com', 'clave')

        response = self.app.post('/usuario/sesion', data={
            'email': 'test@test.com',
            'password': 'clave'
        })

        self.assertEqual(response.status_code, 400)

    def test_iniciar_sesion_content_type_con_charset_devuelve_200(self):
        self.crear_usuario('test@test.com', 'clave')

        response = self.app.post('/usuario/sesion', json={
            'email': 'test@test.com',
            'password': 'clave'
        }, headers={'Content-Type': 'application/json; charset=UTF-8'})

        self.assertEqual(response.status_code, 200)

    def test_validar_token_usuario_deshabilitado_devuelve_401(self):
        usuario = self.crear_usuario('test@test.com', 'clave')

        response = self.app.post('/usuario/sesion', json={
            'email': 'test@test.com',
            'password': 'clave'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.json)
        token = response.json['auth_token']

        usuario.habilitado = False
        db.session.add(usuario)
        db.session.commit()

        response = self.app.get('/usuario/sesion', headers={
            'Authorization': f'Bearer {token}'
        })

        self.assertEqual(response.status_code, 401)



if __name__ == '__main__':
    unittest.main()
