import unittest

from app import app, db
from config import Config
import usuario_api

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config.from_object(Config)
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def crear_usuario(self, email, password):
        usuario = usuario_api.crear_usuario(email, password)
        usuario_api.guardar_usuario(usuario)
        return usuario
