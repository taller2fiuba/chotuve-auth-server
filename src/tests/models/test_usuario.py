import unittest

from app.models.usuario import Usuario
from tests.base import BaseTestCase

class UsuarioTestCase(BaseTestCase):
    def test_generar_auth_token(self):
        usuario = self.crear_usuario('test@test.com', 'test')
        auth_token = usuario.generar_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(Usuario.validar_auth_token(auth_token) == usuario.id)

if __name__ == '__main__':
    unittest.main()
