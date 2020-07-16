import unittest
from unittest.mock import MagicMock
import mock

from tests.base import BaseTestCase
from app import app
from app.generador_token import generar_token_usuario, generar_token_app_server
from app.autenticacion import validar_app_token, validar_admin_token, \
                              requiere_admin, requiere_app_token, requiere_app_token_o_admin

class AutenticacionTestCase(BaseTestCase):
    def test_validar_admin_token_devuelve_false_sin_token(self):
        self.assertFalse(validar_admin_token(None))

    def test_validar_admin_token_devuelve_false_con_token_invalido(self):
        self.assertFalse(validar_admin_token('token-invalido'))

    def test_validar_admin_token_devuelve_true_con_token_correcto(self):
        token = generar_token_usuario(0, True)
        self.assertTrue(validar_admin_token(token))

    def test_validar_app_token_devuelve_false_sin_token(self):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False
        self.assertFalse(validar_app_token(None))

    def test_validar_app_token_devuelve_false_con_token_invalido(self):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False
        self.assertFalse(validar_app_token('token-invalido'))

    @mock.patch('app.models.app_server.AppServer.query')
    def test_validar_app_token_devuelve_true_con_token_correcto(self, mock_query):
        mock_query.filter_by.return_value.one_or_none = MagicMock()
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False
        token = generar_token_app_server(1)
        self.assertTrue(validar_app_token(token))

    def test_validar_app_token_devuelve_true_al_ignorar_tokens(self):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = True

        self.assertTrue(validar_app_token(None))
        self.assertTrue(validar_app_token('token-invalido'))
        token = generar_token_app_server(1)
        self.assertTrue(validar_app_token(token))

    @mock.patch('app.autenticacion.validar_admin_token')
    def test_requiere_admin_decorator_con_token_valido(self, mock_admin):
        @requiere_admin
        def test_func():
            return {'los': 'datos'}, 201

        mock_admin.return_value = True

        with app.test_request_context(headers={'Authorization': 'Bearer token-valido'}):
            data, status_code = test_func()

        mock_admin.assert_called_with('token-valido')
        self.assertEqual({'los': 'datos'}, data)
        self.assertEqual(201, status_code)

    @mock.patch('app.autenticacion.validar_admin_token')
    def test_requiere_admin_decorator_con_token_invalido(self, mock_admin):
        @requiere_admin
        def test_func():
            return {'los': 'datos'}, 201

        mock_admin.return_value = False

        with app.test_request_context(headers={'Authorization': 'Bearer token-invalido'}):
            _, status_code = test_func()

        mock_admin.assert_called_with('token-invalido')
        self.assertEqual(401, status_code)

    @mock.patch('app.autenticacion.validar_admin_token')
    def test_requiere_admin_decorator_sin_token(self, mock_admin):
        @requiere_admin
        def test_func():
            return {'los': 'datos'}, 201

        mock_admin.return_value = False

        with app.test_request_context():
            _, status_code = test_func()

        self.assertEqual(401, status_code)

    @mock.patch('app.autenticacion.validar_app_token')
    def test_requiere_app_decorator_con_token_valido(self, mock_app):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False

        @requiere_app_token
        def test_func():
            return {'los': 'datos'}, 201

        mock_app.return_value = True

        with app.test_request_context(headers={'X-APP-SERVER-TOKEN': 'token-valido'}):
            data, status_code = test_func()

        mock_app.assert_called_with('token-valido')
        self.assertEqual({'los': 'datos'}, data)
        self.assertEqual(201, status_code)

    @mock.patch('app.autenticacion.validar_app_token')
    def test_requiere_app_decorator_con_token_invalido(self, mock_app):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False

        @requiere_app_token
        def test_func():
            return {'los': 'datos'}, 201

        mock_app.return_value = False

        with app.test_request_context(headers={'X-APP-SERVER-TOKEN': 'token-invalido'}):
            _, status_code = test_func()

        mock_app.assert_called_with('token-invalido')
        self.assertEqual(401, status_code)

    @mock.patch('app.autenticacion.validar_app_token')
    def test_requiere_app_decorator_sin_token(self, mock_app):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False

        @requiere_app_token
        def test_func():
            return {'los': 'datos'}, 201

        mock_app.return_value = False

        with app.test_request_context():
            _, status_code = test_func()

        self.assertEqual(401, status_code)

    @mock.patch('app.autenticacion.validar_app_token')
    @mock.patch('app.autenticacion.validar_admin_token')
    def test_requiere_app_o_admin_decorator_con_app_token_valido(self, mock_auth, mock_app):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False

        @requiere_app_token_o_admin
        def test_func():
            return {'los': 'datos'}, 201

        mock_auth.return_value = False
        mock_app.return_value = True

        with app.test_request_context(headers={'X-APP-SERVER-TOKEN': 'token-valido'}):
            data, status_code = test_func()

        mock_app.assert_called_with('token-valido')
        self.assertEqual({'los': 'datos'}, data)
        self.assertEqual(201, status_code)

    @mock.patch('app.autenticacion.validar_app_token')
    @mock.patch('app.autenticacion.validar_admin_token')
    def test_requiere_app_o_admin_decorator_con_app_token_invalido(self, mock_auth, mock_app):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False

        @requiere_app_token_o_admin
        def test_func():
            return {'los': 'datos'}, 201

        mock_auth.return_value = False
        mock_app.return_value = False

        with app.test_request_context(headers={'X-APP-SERVER-TOKEN': 'token-invalido'}):
            _, status_code = test_func()

        mock_app.assert_called_with('token-invalido')
        self.assertEqual(401, status_code)

    @mock.patch('app.autenticacion.validar_app_token')
    @mock.patch('app.autenticacion.validar_admin_token')
    def test_requiere_app_o_admin_decorator_sin_token(self, mock_auth, mock_app):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False

        @requiere_app_token_o_admin
        def test_func():
            return {'los': 'datos'}, 201

        mock_auth.return_value = False
        mock_app.return_value = False

        with app.test_request_context():
            _, status_code = test_func()

        self.assertEqual(401, status_code)

    @mock.patch('app.autenticacion.validar_app_token')
    @mock.patch('app.autenticacion.validar_admin_token')
    def test_requiere_app_o_admin_decorator_con_auth_token_valido(self, mock_auth, mock_app):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False

        @requiere_app_token_o_admin
        def test_func():
            return {'los': 'datos'}, 201

        mock_auth.return_value = True
        mock_app.return_value = False

        with app.test_request_context(headers={'Authorization': 'Bearer token-valido'}):
            data, status_code = test_func()

        mock_auth.assert_called_with('token-valido')
        self.assertEqual({'los': 'datos'}, data)
        self.assertEqual(201, status_code)

    @mock.patch('app.autenticacion.validar_app_token')
    @mock.patch('app.autenticacion.validar_admin_token')
    def test_requiere_app_o_admin_decorator_con_auth_token_invalido(self, mock_auth, mock_app):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False

        @requiere_app_token_o_admin
        def test_func():
            return {'los': 'datos'}, 201

        mock_auth.return_value = False
        mock_app.return_value = False

        with app.test_request_context(headers={'Authorization': 'Bearer token-invalido'}):
            _, status_code = test_func()

        mock_auth.assert_called_with('token-invalido')
        self.assertEqual(401, status_code)

if __name__ == '__main__':
    unittest.main()
