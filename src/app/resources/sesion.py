from flask_restful import Resource
from flask import request

from app.models import Usuario

class SesionResource(Resource):
    def post(self):
        post_data = request.get_json()
        try:
            # Buscar el usuario por email
            usuario = Usuario.query.filter_by(
                email=post_data.get('email')
            ).first()
            if usuario and usuario.verificar_password(post_data.get('password')):
                auth_token = usuario.generar_auth_token()
                return {'auth_token': auth_token.decode()}, 200
            else:
                return {'mensaje': 'Email o constraseña invalidos'}, 400
        except Exception as e:
            # TODO ver esto, no se que podria pasar aca
            return {'mensaje': 'Error'}, 500

    def get(self):
        # obtener el auth_token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            # TODO resta cachear excepciones en caso de token invalido o caducado
            # En ese caso devolver 403
            usuario_id = Usuario.validar_auth_token(auth_token)
            # TODO UsuarioRepositorio
            usuario = Usuario.query.filter_by(id=usuario_id).first()
            return {'usuario_id': usuario_id}, 200
        else:
            # no mandaste auth_token
            return {}, 401
