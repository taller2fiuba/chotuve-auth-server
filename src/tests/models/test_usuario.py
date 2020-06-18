import unittest

from app import db
from app.models.usuario import Usuario
from tests.base import BaseTestCase

class UsuarioTestCase(BaseTestCase):
    def test_generar_auth_token(self):
        usuario = self.crear_usuario('test@test.com', 'test')
        auth_token = usuario.generar_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(Usuario.validar_auth_token(auth_token).id == usuario.id)

    def test_generar_auth_token_deshabilitado(self):
        usuario = self.crear_usuario('test@test.com', 'test')
        usuario.habilitado = False
        db.session.add(usuario)
        db.session.commit()
        auth_token = usuario.generar_auth_token()
        self.assertIsNone(Usuario.validar_auth_token(auth_token))


if __name__ == '__main__':
    unittest.main()
