from flask_restful import Resource
from flask import request

from app import db
from app.autenticacion import requiere_admin
from app.models.app_server import AppServer

OFFSET_POR_DEFECTO = 0
CANTIDAD_POR_DEFECTO = 10

class AppServerResource(Resource):
    @requiere_admin
    def post(self):
        post_data = request.get_json() or {}
        url = post_data.get('url')
        nombre = post_data.get('nombre')

        if not url or not nombre:
            return {'mensaje': 'Falta el nombre y/o la URL.'}, 400

        if AppServer.query.filter_by(url=url).one_or_none():
            return {'mensaje': 'El app server ya se encuentra registrado'}, 400

        app_server = AppServer(url=url, nombre=nombre)
        db.session.add(app_server)
        db.session.commit()
        return {'id': app_server.id, 'token': app_server.generar_token()}, 201

    @requiere_admin
    def get(self, app_id=None):
        if app_id:
            app_server = AppServer.query.filter_by(id=app_id).one_or_none()
            if not app_server:
                return {}, 404

            return app_server.serializar(), 200

        offset = request.args.get('offset', str(OFFSET_POR_DEFECTO))
        cantidad = request.args.get('cantidad', str(CANTIDAD_POR_DEFECTO))
        if not offset.isdigit() or not cantidad.isdigit():
            return {'mensaje': 'El offset y la cantidad deben ser enteros'}, 400

        offset, cantidad = int(offset), int(cantidad)

        data = AppServer.query.offset(offset).limit(cantidad).all()
        return [app_server.serializar() for app_server in data], 200

    @requiere_admin
    def delete(self, app_id):
        app_server = AppServer.query.filter_by(id=app_id).one_or_none()
        if not app_server:
            return {}, 404

        db.session.delete(app_server)
        db.session.commit()
        return {}, 200
