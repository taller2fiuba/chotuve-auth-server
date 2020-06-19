from flask_restful import Resource

class PingResource(Resource):
    def get(self):
        return {}, 200
