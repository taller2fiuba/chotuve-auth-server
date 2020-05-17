from flask_restful import Resource
from flask import request

import usuario_api

class UsuarioCrearResource(Resource):
    def post(self):
        post_data = request.get_json()
        mail = post_data.get('email')
        password = post_data.get('password')

        if not usuario_api.usuario_existente(mail=mail):
            usuario = usuario_api.crear_usuario(mail, password)
            usuario_api.guardar_usuario(usuario)
            auth_token = usuario.generar_auth_token()
            return {'auth_token': auth_token.decode()}, 201
        return {'errores': {'email': 'El mail ya se encuentra registrado'}}, 400

class UsuarioResource(Resource):
    def get(self, usuario_id):
        if usuario_api.usuario_existente(usuario_id=usuario_id):
            usuario = usuario_api.cargar_usuario(usuario_id=usuario_id)
            return {'email': usuario.email}, 200
        return {}, 404
