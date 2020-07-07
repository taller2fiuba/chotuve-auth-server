from flask_restful import Resource
from flask import request
import flask_sqlalchemy

from app import db
from app.models.usuario import Usuario

OFFSET_POR_DEFECTO = 0
CANTIDAD_POR_DEFECTO = 10

class UsuarioResource(Resource):
    def post(self):
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')

        # TODO ver como hacer las validaciones de una forma copada, no tener que hacer todo a mano
        if not Usuario.query.filter_by(email=email).one_or_none():
            usuario = Usuario(email=email, password=password)
            db.session.add(usuario)
            db.session.commit()
            auth_token = usuario.generar_auth_token()
            return {'auth_token': auth_token.decode(), 'id': usuario.id}, 201
        return {'errores': {'email': 'El mail ya se encuentra registrado'}}, 400

    def get(self):
        try:
            ids = request.args.get('ids', None)
            offset = request.args.get('offset', OFFSET_POR_DEFECTO)
            cantidad = request.args.get('cantidad', CANTIDAD_POR_DEFECTO)
            if not ids:
                usuarios = Usuario.query.offset(offset).limit(cantidad).all()
            else:
                ids = [int(i) for i in ids.split(',')]
                usuarios = Usuario.query.filter(Usuario.id.in_((ids)))
            return list(map(lambda usuario: usuario.serializar(), usuarios)), 200
        except flask_sqlalchemy.orm.exc.NoResultFound:
            return {}, 404
        except ValueError:
            return {}, 400
