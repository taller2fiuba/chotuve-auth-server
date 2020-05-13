# TODO sacar la logica jwt, poner en un servicio
import jwt
import datetime

# TODO sacar la logica bcrypt, poner en un servicio
from app import app, db, bcrypt

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    registro_fecha_hora = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.email}>'

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.registro_fecha_hora = datetime.datetime.now()

    def verificar_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generar_auth_token(self):
        try:
            # contenido encriptado del token jwt
            payload = {
                # expira dentro de un dia
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                # generado ahora
                'iat': datetime.datetime.utcnow(),
                # corresponde a este usuario
                'sub': self.id
            }
            return jwt.encode(
                payload,
                app.config.get('AUTH_TOKEN_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def validar_auth_token(auth_token):
        "Valida un auth token y devuelve el id de usuario que fue puesto dentro de él"
        try:
            payload = jwt.decode(auth_token, app.config.get('AUTH_TOKEN_KEY'))
            return payload['sub']
