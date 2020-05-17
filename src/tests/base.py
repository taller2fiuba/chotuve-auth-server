import unittest

from app import app, db
from app.models.usuario import Usuario
from config import Config

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
        usuario = Usuario(
            email=email,
            password=password
        )
        # TODO UsuarioRepositorio
        db.session.add(usuario)
        db.session.commit()
        return usuario
