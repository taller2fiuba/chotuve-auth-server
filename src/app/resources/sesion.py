from flask_restful import Resource
from flask import request
import jwt

from app.models.usuario import Usuario

class SesionResource(Resource):
    def post(self):
        post_data = request.get_json()
        # Buscar el usuario por email
        usuario = Usuario.query.filter_by(
            email=post_data.get('email')
        ).first()
        if usuario and usuario.verificar_password(post_data.get('password')):
            auth_token = usuario.generar_auth_token()
            return {'auth_token': auth_token.decode()}, 200
        return {'mensaje': 'Email o constraseña invalidos'}, 400

    def get(self):
        auth_header = request.headers.get('Authorization')
        auth_token = ''
        if auth_header:
            # el auth_token esta despues Bearer
            split = auth_header.split(" ")
            if len(split) == 2 and split[0] == 'Bearer':
                auth_token = split[1]
        if auth_token:
            try:
                usuario_id = Usuario.validar_auth_token(auth_token)
                return {'usuario_id': usuario_id}, 200
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                # token invalido o caducado
                return {}, 403
        # no mandaste auth_token
        return {}, 401
