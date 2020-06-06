from flask_restful import Resource
from flask import request
import flask_sqlalchemy

from app import db

from app.models.usuario import Usuario

class UsuarioIdResource(Resource):
    def get(self, usuario_id):
        try:
            usuario = Usuario.query.filter_by(id=usuario_id).one()
            return usuario.serializar(), 200
        except flask_sqlalchemy.orm.exc.NoResultFound:
            return {}, 404

    def put(self, usuario_id):
        try:
            usuario = Usuario.query.filter_by(id=usuario_id).one()
            post_data = request.get_json()
            usuario.nombre = post_data['nombre']
            usuario.apellido = post_data['apellido']
            usuario.telefono = post_data['telefono']
            usuario.direccion = post_data['direccion']

            db.session.commit()

            return {}, 200
        except flask_sqlalchemy.orm.exc.NoResultFound:
            return {}, 404
