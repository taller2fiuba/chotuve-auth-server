from flask_restful import Resource

from app import db

class BaseDeDatosResource(Resource):
    # TODO solo en dev
    def delete(self):
        meta = db.metadata
        for tabla in reversed(meta.sorted_tables):
            # TODO logger
            print(f'Limpiando tabla {tabla}')
            db.session.execute(tabla.delete())
        db.session.commit()
        return {}, 200
