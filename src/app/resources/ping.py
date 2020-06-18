from flask_restful import Resource
from app.middleware.cors import habilitar_cors

class PingResource(Resource):
    @habilitar_cors
    def get(self):
        return {}, 200
