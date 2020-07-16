from app import db, generador_token

class AppServer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<AppServer {self.url}>'

    def generar_token(self):
        return generador_token.generar_token_app_server(self.id)

    def serializar(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'url': self.url
        }

    @staticmethod
    def validar_token(token):
        """
        Valida un token de app server. Si es válido devuelve la entidad app server
        correspondiente, en caso contrario devuelve None.
        """
        app_id = generador_token.decodificar_token(token).get('app_id')
        if not app_id:
            return None
        return AppServer.query.filter_by(id=app_id).one_or_none()
