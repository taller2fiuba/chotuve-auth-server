import unittest
import json

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

    def post(self, url, data):
        response = self.app.post(url,
                                 data=json.dumps(data),
                                 content_type='application/json')
        return response, self.get_response_json(response)

    def get_response_json(self, response):
        return json.loads(response.data.decode())

    def crear_usuario(self, email, password):
        usuario = Usuario(
            email=email,
            password=password
        )
        # TODO UsuarioRepositorio
        db.session.add(usuario)
        db.session.commit()
        return usuario
