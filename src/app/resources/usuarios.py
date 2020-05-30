from flask_restful import Resource
from flask import request
import flask_sqlalchemy


from app.models.usuario import Usuario

class UsuariosResource(Resource):
    def get(self):
        try:
            ids = request.args.get('ids', None)
            offset = request.args.get('offset', 0)
            cantidad = request.args.get('cantidad', 10)
            if not ids:
                usuarios = Usuario.query.offset(offset).limit(cantidad).all()
            else:
                ids = [int(i) for i in ids.split(',')]
                usuarios = Usuario.query.filter(Usuario.id.in_((ids)))
            return list(map(lambda dev: dev.serializar(), usuarios)), 200
        except flask_sqlalchemy.orm.exc.NoResultFound:
            return {}, 404
        except ValueError:
            return {}, 400
