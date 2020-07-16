import unittest
import mock

from app import app
from tests.base import BaseTestCase

class AppServerTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        patcher = mock.patch('app.autenticacion.validar_admin_token')
        mock_validar_admin_token = patcher.start()
        mock_validar_admin_token.return_value = True
        self.addCleanup(patcher.stop)

    def test_get_devuelve_vacio_sin_app_servers(self):
        response = self.app.get('/app-server')
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    def test_get_devuelve_app_servers(self):
        self.app.post('/app-server', json={'url': 'url', 'nombre': 'nombre'})

        response = self.app.get('/app-server')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json))
        self.assertEqual('url', response.json[0]['url'])
        self.assertEqual('nombre', response.json[0]['nombre'])

    def test_get_devuelve_400_en_paginado_erroneo(self):
        response = self.app.get('/app-server?offset=casa&cantidad=coso')
        self.assertEqual(400, response.status_code)

    def test_get_devuelve_app_server_por_id(self):
        r = self.app.post('/app-server', json={'url': 'url', 'nombre': 'nombre'})
        app_id = r.json['id']

        response = self.app.get(f'/app-server/{app_id}')
        self.assertEqual(200, response.status_code)
        self.assertEqual('url', response.json['url'])
        self.assertEqual('nombre', response.json['nombre'])

    def test_get_devuelve_404_en_id_inexistente(self):
        response = self.app.get('/app-server/123')
        self.assertEqual(404, response.status_code)

    def test_post_devuelve_nuevo_token_de_app_server(self):
        response = self.app.post('/app-server', json={'url': 'url', 'nombre': 'nombre'})
        self.assertEqual(201, response.status_code)
        self.assertIn('token', response.json)

    def test_post_devuelve_400_si_ya_existe_url(self):
        response = self.app.post('/app-server', json={'url': 'url', 'nombre': 'nombre'})
        response = self.app.post('/app-server', json={'url': 'url', 'nombre': 'nombre'})
        self.assertEqual(400, response.status_code)

    def test_post_devuelve_400_si_faltan_datos(self):
        response = self.app.post('/app-server', json={'url': 'url'})
        self.assertEqual(400, response.status_code)
        response = self.app.post('/app-server', json={'nombre': 'nombre'})
        self.assertEqual(400, response.status_code)
        response = self.app.post('/app-server')
        self.assertEqual(400, response.status_code)

    def test_delete_devuelve_404_si_no_existe_app_server(self):
        response = self.app.delete('/app-server/123')
        self.assertEqual(404, response.status_code)

    def test_delete_elimina_app_server_correctamente(self):
        r = self.app.post('/app-server', json={'url': 'url', 'nombre': 'nombre'})
        app_id = r.json['id']

        response = self.app.delete(f'/app-server/{app_id}')
        self.assertEqual(200, response.status_code)

    def test_get_sesion_devuelve_200_en_token_valido(self):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False

        r = self.app.post('/app-server', json={'url': 'url', 'nombre': 'nombre'})
        self.assertEqual(201, r.status_code)
        app_token = r.json['token']

        response = self.app.get('/app-server/sesion', headers={'X-APP-SERVER-TOKEN': app_token})
        self.assertEqual(200, response.status_code)

    def test_get_sesion_devuelve_401_en_token_invalido(self):
        app.config['IGNORAR_APP_SERVER_TOKEN'] = False

        response = self.app.get('/app-server/sesion', headers={'X-APP-SERVER-TOKEN': 'invalido'})
        self.assertEqual(401, response.status_code)

if __name__ == '__main__':
    unittest.main()
