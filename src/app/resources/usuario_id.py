from flask_restful import Resource
import flask_sqlalchemy


from app.models.usuario import Usuario

class UsuarioIdResource(Resource):
    def get(self, usuario_id):
        try:
            usuario = Usuario.query.filter_by(id=usuario_id).one()
            return {'email': usuario.email}, 200
        except flask_sqlalchemy.orm.exc.NoResultFound:
            return {}, 404
