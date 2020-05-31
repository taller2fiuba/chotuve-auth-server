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
API = Api(app)

from .resources import ping, usuario, usuarios, sesion, base_de_datos

API.add_resource(ping.PingResource, '/ping')
API.add_resource(usuario.UsuarioResource, '/usuario', methods=["POST"])
API.add_resource(usuarios.UsuariosResource, '/usuario', methods=["GET"], endpoint='Usuarios')
API.add_resource(usuario.UsuarioResource, '/usuario/<int:usuario_id>', methods=["GET"], endpoint='UsuarioConIdResource')
API.add_resource(sesion.SesionResource, '/usuario/sesion')
API.add_resource(base_de_datos.BaseDeDatosResource, '/base_de_datos')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
