import datetime
import jwt
from flask_restful import Resource
from flask import request

from app import app

ADMIN_EMAIL = app.config.get('ADMIN_EMAIL')
ADMIN_CLAVE = app.config.get('ADMIN_CLAVE')

class UsuarioAdminResource(Resource):
    def post(self):
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        if not email or not password:
            return {'error': 'Falta el e-mail o la clave'}, 400

        if ADMIN_EMAIL != email or ADMIN_CLAVE != password:
            return {'error': 'Credenciales inválidas'}, 401

        auth_token = self._generar_admin_token()
        return {'auth_token': auth_token.decode()}, 200

    def _generar_admin_token(self):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365*10),
            'iat': datetime.datetime.utcnow(),
            'sub': {
                'uid': 0,
                'es_admin': True
            }
        }
        return jwt.encode(payload, app.config.get('JWT_SECRET_KEY'), algorithm='HS256')
