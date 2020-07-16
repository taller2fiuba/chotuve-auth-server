from flask_restful import Resource
from flask import request

from app import app
from app.generador_token import generar_token_usuario

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

        return {'auth_token': generar_token_usuario(0, True)}, 200
