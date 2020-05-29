# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_mail_registrado import ErrorMailRegistrado  # noqa: E501
from swagger_server.models.mail_usuario import MailUsuario  # noqa: E501
from swagger_server.models.mensaje_campo_invalido import MensajeCampoInvalido  # noqa: E501
from swagger_server.models.token import Token  # noqa: E501
from swagger_server.models.usuario import Usuario  # noqa: E501
from swagger_server.models.usuario_id import UsuarioId  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_base_de_datos_delete(self):
        """Test case for base_de_datos_delete

        Elimina todas las tablas de la base de datos
        """
        response = self.client.open(
            '/Chotuve1/chotuveAuthServer/1.0.0/base_de_datos',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pin_get(self):
        """Test case for pin_get

        Ping del App Server
        """
        response = self.client.open(
            '/Chotuve1/chotuveAuthServer/1.0.0/pin',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_usuario_get(self):
        """Test case for usuario_get

        Devuelve el email del usuario correspondiente
        """
        response = self.client.open(
            '/Chotuve1/chotuveAuthServer/1.0.0/usuario'.format(usuario_id='usuario_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_usuario_post(self):
        """Test case for usuario_post

        Crea un nuevo usuario
        """
        nuevo_usuario = Usuario()
        response = self.client.open(
            '/Chotuve1/chotuveAuthServer/1.0.0/usuario',
            method='POST',
            data=json.dumps(nuevo_usuario),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_usuario_sesion_get(self):
        """Test case for usuario_sesion_get

        Validar token de sesion
        """
        headers = [('Authorization', 'Authorization_example')]
        response = self.client.open(
            '/Chotuve1/chotuveAuthServer/1.0.0/usuario/sesion',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_usuario_sesion_post(self):
        """Test case for usuario_sesion_post

        Inicio de sesion
        """
        usuario = UsuarioId()
        response = self.client.open(
            '/Chotuve1/chotuveAuthServer/1.0.0/usuario/sesion',
            method='POST',
            data=json.dumps(usuario),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
