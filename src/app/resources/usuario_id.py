from flask_restful import Resource
from flask import g, request
import flask_sqlalchemy

from app import db
from app.autenticacion import requiere_app_token_o_admin
from app.models.usuario import Usuario

class UsuarioIdResource(Resource):
    @requiere_app_token_o_admin
    def get(self, usuario_id):
        try:
            usuario = Usuario.query.filter_by(id=usuario_id).one()
            return usuario.serializar(), 200
        except flask_sqlalchemy.orm.exc.NoResultFound:
            return {}, 404

    @requiere_app_token_o_admin
    def put(self, usuario_id):
        usuario = Usuario.query.filter_by(id=usuario_id).one_or_none()
        if not usuario:
            return {}, 404

        post_data = request.get_json()
        if 'nombre' in post_data:
            usuario.nombre = post_data['nombre']
        if 'apellido' in post_data:
            usuario.apellido = post_data['apellido']
        if 'telefono' in post_data:
            usuario.telefono = post_data['telefono']
        if 'direccion' in post_data:
            usuario.direccion = post_data['direccion']
        if 'foto' in post_data:
            usuario.foto = post_data['foto']
        if 'habilitado' in post_data:
            if not g.es_admin:
                return {'mensaje': 'Requiere admin'}, 403
            usuario.habilitado = bool(post_data['habilitado'])

        db.session.commit()
        return {}, 200
