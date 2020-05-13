#pylint: skip-file
from flask import Flask
from flask_restful import Api
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
API = Api(app)

from .resources import ping, usuario, sesion

API.add_resource(ping.PingResource, '/ping')
API.add_resource(usuario.UsuarioResource, '/usuario')
API.add_resource(sesion.SesionResource, '/usuario/sesion')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
