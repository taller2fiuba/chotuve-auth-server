import unittest
import mock

from app import db
from app.models.usuario import Usuario
from tests.base import BaseTestCase

class UsuarioTestCase(BaseTestCase):
    def test_generar_auth_token(self):
        usuario = self.crear_usuario('test@test.com', 'test')
        auth_token = usuario.generar_auth_token()
        self.assertTrue(isinstance(auth_token, str))
        data = Usuario.validar_auth_token(auth_token)
        self.assertIsNotNone(data)
        self.assertEqual(data[0].id, usuario.id)
        self.assertFalse(data[1])

    def test_generar_auth_token_deshabilitado(self):
        usuario = self.crear_usuario('test@test.com', 'test')
        usuario.habilitado = False
        db.session.add(usuario)
        db.session.commit()
        auth_token = usuario.generar_auth_token()
        self.assertIsNone(Usuario.validar_auth_token(auth_token))

    @mock.patch('app.models.usuario.Usuario.query')
    def test_cantidad_de_usuarios(self, mock_db):
        mock_db.count.return_value = 0
        self.assertEqual(Usuario.cantidad_usuarios(), 0)

if __name__ == '__main__':
    unittest.main()
