from flask_restful import Resource

from app.models.usuario import Usuario

class HistoricoResource(Resource):
    #@requiere_app_token
    def get(self):
        return {"total_usuarios": Usuario.cantidad_usuarios()}, 200
