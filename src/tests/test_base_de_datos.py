import unittest

from app import app, db, models
from config import Config

class BaseDeDatosTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config.from_object(Config)

    def test_delete_base_de_datos_exitoso(self):
        usuario = models.Usuario(
            email='email',
            password='password'
        )
        db.session.add(usuario)
        db.session.commit()
        self.assertEqual(db.session.query(models.Usuario).count(), 1)
        response = self.app.delete('/base_de_datos')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(db.session.query(models.Usuario).count(), 0)

if __name__ == '__main__':
    unittest.main()
