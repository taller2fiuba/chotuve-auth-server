import unittest
import mock

from tests.base import BaseTestCase

class UsuariosResourceTestCase(BaseTestCase):
    def test_get_usuario_existente(self):
        usuario = self.crear_usuario('test@test.com', '123456')
        response = self.app.get(f'/usuario/{usuario.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], usuario.email)

    def test_get_usuario_inexistente(self):
        id_no_existe = 15121
        response = self.app.get(f'/usuario/{id_no_existe}')
        self.assertEqual(response.status_code, 404)

    @mock.patch('app.autenticacion.validar_admin_token')
    def test_puede_deshabilitar_si_es_admin(self, mock_admin):
        usuario = self.crear_usuario('test@test.com', '123456')
        mock_admin.return_value = True
        response = self.app.put(f'/usuario/{usuario.id}', json={'habilitado': False})
        self.assertEqual(200, response.status_code)

    @mock.patch('app.autenticacion.validar_admin_token')
    def test_no_puede_deshabilitar_si_no_es_admin(self, mock_admin):
        usuario = self.crear_usuario('test@test.com', '123456')
        mock_admin.return_value = False
        response = self.app.put(f'/usuario/{usuario.id}', json={'habilitado': False})
        self.assertEqual(403, response.status_code)

if __name__ == '__main__':
    unittest.main()
