import unittest
import mock

from tests.base import BaseTestCase
from app import app
from app.models.usuario import Usuario

class UsuarioResourceTestCase(BaseTestCase):
    def test_registracion_exitosa(self):
        response = self.app.post('/usuario', json={
            'email': 'test@test.com',
            'password': '123456'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json['auth_token'])
        self.assertTrue(response.json['id'], 1)

    def test_registracion_fallida_ya_registrado(self):
        self.crear_usuario('test@test.com', '123456')
        response = self.app.post('/usuario', json={
            'email': 'test@test.com',
            'password': '123456'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json['errores']['email'] == 'El mail ya se encuentra registrado')

    def test_registracion_fallida_ya_registrado_con_admin_email(self):
        response = self.app.post('/usuario', json={
            'email': app.config.get('ADMIN_EMAIL'),
            'password': '123456'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json['errores']['email'] == 'El mail ya se encuentra registrado')

    def test_get_usuarios_sin_usuarios_registrados(self):
        response = self.app.get('/usuario')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(not response.json)

    def test_get_usuarios_con_usuarios_registrados(self):
        self.crear_usuario('test@test.com', '123456')
        self.crear_usuario('test2@test.com', '123456')
        self.crear_usuario('test3@test.com', '123456')

        response = self.app.get('/usuario')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)


    def test_get_usuarios_con_ids_inexistentes(self):
        self.crear_usuario('test@test.com', '123456')

        response = self.app.get('/usuario?ids=2')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(not response.json)

    def test_get_usuarios_con_ids_existentes(self):
        emails = ['a@test.com', 'b@test.com', 'c@test.com', 'd@test.com']
        for email in emails:
            self.crear_usuario(email, '123456')

        response = self.app.get('/usuario?ids=2,3')
        email_response = [usuario['email'] for usuario in response.json]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertListEqual(email_response, ['b@test.com', 'c@test.com'])

    def test_get_usuarios_con_ids_invalidos(self):
        response = self.app.get('/usuario?ids=a')
        self.assertEqual(response.status_code, 400)

    def test_get_usuarios_con_ids_repetidos(self):
        emails = ['a@test.com', 'b@test.com', 'c@test.com', 'd@test.com']
        for email in emails:
            self.crear_usuario(email, '123456')

        response = self.app.get('/usuario?ids=1,1,3,3,3')
        email_response = [usuario['email'] for usuario in response.json]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertListEqual(email_response, ['a@test.com', 'c@test.com'])


    def test_put_actualizar_perfil_exitosamente(self):
        usuario = self.crear_usuario('test2@test.com', '1234567')
        nuevo_nombre = "Lucas"
        nuevo_apellido = "Perez"
        nueva_direccion = "La Pampa 1111"
        nuevo_telefono = "1530449926"
        response = self.app.put('/usuario/'+str(usuario.id), json={
            'nombre': nuevo_nombre,
            'apellido': nuevo_apellido,
            'telefono': nuevo_telefono,
            'direccion': nueva_direccion})

        usuario = Usuario.query.filter_by(email="test2@test.com").one_or_none()

        self.assertEqual(usuario.nombre, nuevo_nombre)
        self.assertEqual(usuario.apellido, nuevo_apellido)
        self.assertEqual(usuario.direccion, nueva_direccion)
        self.assertEqual(usuario.telefono, nuevo_telefono)
        self.assertEqual(response.status_code, 200)

    def test_put_actualizar_perfil_id_inexistente(self):
        id_no_existe = 15121
        nuevo_nombre = "Lucas"
        nuevo_apellido = "Perez"
        nueva_direccion = "La Pampa 1111"
        nuevo_telefono = "1530449926"
        response = self.app.put('/usuario/'+str(id_no_existe), json={
            'nombre': nuevo_nombre,
            'apellido': nuevo_apellido,
            'telefono': nuevo_telefono,
            'direccion': nueva_direccion})
        self.assertEqual(response.status_code, 404)

    def test_get_perfil_existente(self):
        usuario = self.crear_usuario('test2@test.com', '1234567')
        response = self.app.get('/usuario/'+str(usuario.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 1,
                                         'nombre': None,
                                         'apellido': None,
                                         'email': 'test2@test.com',
                                         'telefono': None,
                                         'direccion': None,
                                         'foto': None,
                                         'habilitado': True})

    def test_get_perfil_todos_los_campos_modificado_existente(self):
        usuario = self.crear_usuario('test2@test.com', '1234567')
        nuevo_nombre = "Lucas"
        nuevo_apellido = "Perez"
        nueva_direccion = "La Pampa 1111"
        nuevo_telefono = "1530449926"
        response = self.app.put('/usuario/'+str(usuario.id), json={
            'nombre': nuevo_nombre,
            'apellido': nuevo_apellido,
            'telefono': nuevo_telefono,
            'direccion': nueva_direccion})
        #actualizo usuario porque la base de datos cierra la sesion despues del put
        usuario = Usuario.query.filter_by(email="test2@test.com").one_or_none()

        response = self.app.get('/usuario/'+str(usuario.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': usuario.id,
                                         'nombre': usuario.nombre,
                                         'apellido': usuario.apellido,
                                         'email': usuario.email,
                                         'telefono': usuario.telefono,
                                         'direccion': usuario.direccion,
                                         'foto': None,
                                         'habilitado': True})

    def test_get_perfil_parcialmente_modificado_existente(self):
        usuario = self.crear_usuario('test2@test.com', '1234567')
        nuevo_nombre = "Lucas"
        nuevo_apellido = "Perez"
        nueva_direccion = None
        nuevo_telefono = "1530449926"
        response = self.app.put('/usuario/'+str(usuario.id), json={
            'nombre': nuevo_nombre,
            'apellido': nuevo_apellido,
            'telefono': nuevo_telefono,
            'direccion': nueva_direccion})
        #actualizo usuario porque la base de datos cierra la sesion despues del put
        usuario = Usuario.query.filter_by(email="test2@test.com").one_or_none()

        response = self.app.get('/usuario/'+str(usuario.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': usuario.id,
                                         'nombre': usuario.nombre,
                                         'apellido': usuario.apellido,
                                         'email': usuario.email,
                                         'telefono': usuario.telefono,
                                         'direccion': usuario.direccion,
                                         'foto': None,
                                         'habilitado': True})

    def test_get_perfil_inexistente(self):
        id_no_existe = 15121
        response = self.app.get('/usuario/'+str(id_no_existe))
        self.assertEqual(response.status_code, 404)

    @mock.patch('app.autenticacion.validar_admin_token')
    def test_deshabilitar_usuario(self, mock_admin):
        usuario = self.crear_usuario('test2@test.com', '1234567')
        mock_admin.return_value = True
        response = self.app.put('/usuario/'+str(usuario.id), json={
            'habilitado': False
        })

        usuario = Usuario.query.filter_by(email="test2@test.com").one_or_none()

        response = self.app.get('/usuario/'+str(usuario.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': usuario.id,
                                         'nombre': usuario.nombre,
                                         'apellido': usuario.apellido,
                                         'email': usuario.email,
                                         'telefono': usuario.telefono,
                                         'direccion': usuario.direccion,
                                         'foto': None,
                                         'habilitado': False})

if __name__ == '__main__':
    unittest.main()
