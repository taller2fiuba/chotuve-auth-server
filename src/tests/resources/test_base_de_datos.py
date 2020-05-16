import unittest

from app import db
from app.models.usuario import Usuario
from tests.base import BaseTestCase

class BaseDeDatosTestCase(BaseTestCase):
    def test_delete_base_de_datos_exitoso(self):
        self.crear_usuario('email', 'password')
        self.assertEqual(db.session.query(Usuario).count(), 1)
        response = self.app.delete('/base_de_datos')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(db.session.query(Usuario).count(), 0)

if __name__ == '__main__':
    unittest.main()
