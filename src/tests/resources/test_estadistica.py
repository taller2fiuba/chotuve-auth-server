import unittest
import mock

from tests.base import BaseTestCase

class EstadisticaResourceTestCase(BaseTestCase):
    @mock.patch('app.models.usuario.Usuario.query')
    def test_cantidad_de_usuarios(self, mock_db):
        mock_db.count.return_value = 0

        response = self.app.get('/stats/historico')
        estadisticas = response.json
        self.assertEqual(estadisticas["total_usuarios"], 0)

if __name__ == '__main__':
    unittest.main()
