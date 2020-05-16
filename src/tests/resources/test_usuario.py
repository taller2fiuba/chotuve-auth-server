import unittest
import json

from app import db
from app.models.usuario import Usuario
from tests.base import BaseTestCase

class UsuarioResourceTestCase(BaseTestCase):
    def test_registracion_exitosa(self):
        response = self.app.post('/usuario',
                                 data=json.dumps({
                                     'email': 'test@test.com',
                                     'password': '123456'
                                 }),
                                 content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['auth_token'])

    def test_registracion_fallida_ya_registrado(self):
        usuario = Usuario(
            email='test@test.com',
            password='123456'
        )
        # TODO UsuarioRepositorio
        db.session.add(usuario)
        db.session.commit()
        response = self.app.post('/usuario',
                                 data=json.dumps({
                                     'email': 'test@test.com',
                                     'password': '123456'
                                 }),
                                 content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['errores']['email'] == 'El mail ya se encuentra registrado')

if __name__ == '__main__':
    unittest.main()
