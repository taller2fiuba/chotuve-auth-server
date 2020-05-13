from flask_restful import Resource
from flask import request

from app.models import Usuario

class UsuarioResource(Resource):
    def post(self):
        post_data = request.get_json()
        # verificar que el no exista un usuario con el mismo email
        # TODO ver como hacer las validaciones de una forma copada, no tener que hacer todo a mano
        # TODO UsuarioRepositorio
        usuario = Usuario.query.filter_by(email=post_data.get('email')).first()
        if not usuario:
            try:
                usuario = Usuario(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # Guardar el usuario
                # TODO UsuarioRepositorio
                db.session.add(usuario)
                db.session.commit()
                # generar el token de autenficacion
                auth_token = usuario.generar_auth_token()
                return {'auth_token': auth_token.decode()}, 201
            except Exception as e:
                # TODO mejorar mensaje de error, no se bien porque es este error, quizas deberia ser un 500
                return {'mensaje': 'Error'}, 400
        else:
            # TODO mejorar esto, los errores no van asi, mirar en media server
            return {'mensaje': 'El mail ya se encuentra registrado'}, 400
