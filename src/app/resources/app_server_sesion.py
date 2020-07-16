import jwt
from flask_restful import Resource
from flask import request, abort

from app.models.app_server import AppServer

class AppServerSesionResource(Resource):
    def get(self):
        app_token = request.headers.get('X-APP-SERVER-TOKEN')
        try:
            if not app_token or not AppServer.validar_token(app_token):
                return {}, 401
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(401)

        return {}, 200
