from flask_restful import Resource
from flask import request

from app.repositorios import usuario_repositorio
from app.excepciones import NoExisteEntidadBuscadaException
from app.models.usuario import Usuario

class UsuarioResource(Resource):
    def post(self):
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        # TODO ver como hacer las validaciones de una forma copada, no tener que hacer todo a mano
        if not usuario_repositorio.buscar_unico(False, email=email):
            usuario = Usuario(email=email, password=password)
            usuario_repositorio.guardar(usuario)
            auth_token = usuario.generar_auth_token()
            return {'auth_token': auth_token.decode()}, 201
        return {'errores': {'email': 'El mail ya se encuentra registrado'}}, 400

    def get(self, usuario_id):
        try:
            usuario = usuario_repositorio.buscar_unico(True, id=usuario_id)
            return {'email': usuario.email}, 200
        except NoExisteEntidadBuscadaException:
            return {}, 404
