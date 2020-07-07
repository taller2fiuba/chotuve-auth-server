from flask_restful import Resource
from flask import request, abort
import jwt

from app.models.usuario import Usuario

class SesionResource(Resource):
    def post(self):
        if not 'application/json' in request.content_type:
            abort(400)

        data = request.get_json()
        email, clave = data.get('email'), data.get('password')
        if not email or not clave:
            abort(400)

        usuario = Usuario.query.filter_by(
            email=email,
            habilitado=True
        ).one_or_none()

        if not usuario or not usuario.verificar_password(clave):
            # TODO: Esto debería ser un 401
            return {'mensaje': 'Email o constraseña invalidos'}, 400

        auth_token = usuario.generar_auth_token()
        return {'auth_token': auth_token.decode(), 'id': usuario.id}, 200

    def get(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            abort(401)

        _, token = auth_header.split(' ')[:2]

        try:
            usuario = Usuario.validar_auth_token(token)
            if not usuario:
                abort(401)
            return {'usuario_id': usuario.id}, 200
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(401)
