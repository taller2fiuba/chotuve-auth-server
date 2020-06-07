#pylint: skip-file
from flask import Flask
from flask_restful import Api
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)

from .resources import ping, usuario, usuario_id, sesion, base_de_datos

api.add_resource(ping.PingResource, '/ping')
api.add_resource(usuario.UsuarioResource, '/usuario')
api.add_resource(usuario_id.UsuarioIdResource, '/usuario/<int:usuario_id>')
api.add_resource(sesion.SesionResource, '/usuario/sesion')
api.add_resource(base_de_datos.BaseDeDatosResource, '/base_de_datos')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
