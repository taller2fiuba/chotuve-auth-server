#pylint: skip-file
from flask import Flask
from flask_restful import Api
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config

from .resources import PingResource, UsuarioResource, SesionResource

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
API = Api(app)

API.add_resource(PingResource, '/ping')
API.add_resource(UsuarioResource, '/usuario')
API.add_resource(SesionResource, '/usuario/sesion')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

from app import models
