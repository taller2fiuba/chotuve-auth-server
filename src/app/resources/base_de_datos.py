from flask_restful import Resource

from app import app, db

class BaseDeDatosResource(Resource):
    if app.config.get('FLASK_ENV') == 'development':
        def delete(self):
            meta = db.metadata
            for tabla in reversed(meta.sorted_tables):
                # TODO logger
                print(f'Limpiando tabla {tabla}')
                db.session.execute(tabla.delete())
            db.session.commit()
            return {}, 200
