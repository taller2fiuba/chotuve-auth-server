from flask_restful import Resource
from flask import request

from app import db
from app.autenticacion import requiere_app_token_o_admin
from app.models.usuario import Usuario

class UsuarioClaveResource(Resource):
    @requiere_app_token_o_admin
    def put(self, usuario_id):
        post_data = request.get_json()
        password = post_data.get('password')

        if not password:
            return {}, 400

        usuario = Usuario.query.filter_by(id=usuario_id).one_or_none()
        if not usuario:
            return {}, 404

        usuario.actualizar_clave(password)
        db.session.commit()
        return {}, 200
