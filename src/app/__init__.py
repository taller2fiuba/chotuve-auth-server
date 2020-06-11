#pylint: skip-file
from flask import Flask
from flask_restful import Api
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config, configurar_logger
import logging

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)

configurar_logger()
log = logging.getLogger(__name__)

from .resources import ping, usuario, usuario_id, sesion, base_de_datos

api.add_resource(ping.PingResource, '/ping')
api.add_resource(usuario.UsuarioResource, '/usuario')
api.add_resource(usuario_id.UsuarioIdResource, '/usuario/<int:usuario_id>', methods=["GET", "PUT"])
api.add_resource(sesion.SesionResource, '/usuario/sesion')
api.add_resource(base_de_datos.BaseDeDatosResource, '/base_de_datos')

@app.errorhandler(Exception)
def unhandled_exception(e):
    tb = traceback.format_exc()
    log.warn(f'Excepcion no manejada: {tb}')
    return {'mensaje': str(e)}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

log.info(f'Iniciando version de la app: {Config.APP_VERSION}')