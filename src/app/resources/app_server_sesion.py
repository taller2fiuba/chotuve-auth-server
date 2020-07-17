from flask_restful import Resource
from flask import request

from app.autenticacion import validar_app_token

class AppServerSesionResource(Resource):
    def get(self):
        if not validar_app_token(request.headers.get('X-APP-SERVER-TOKEN')):
            return {}, 401
        return {}, 200
