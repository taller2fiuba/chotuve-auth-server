import datetime
import jwt

from app import app, db, bcrypt

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=True)
    apellido = db.Column(db.String(255), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(255), nullable=True)
    foto = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Usuario {self.email}>'

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.registro_fecha_hora = datetime.datetime.now()

    def verificar_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generar_auth_token(self):
        # contenido encriptado del token jwt
        payload = {
            # expira dentro de 10 años
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365*10),
            # generado ahora
            'iat': datetime.datetime.utcnow(),
            # corresponde a este usuario
            'sub': self.id
        }
        return jwt.encode(
            payload,
            app.config.get('JWT_SECRET_KEY'),
            algorithm='HS256'
        )

    def serializar(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'direccion' : self.direccion,
            'telefono': self.telefono,
            'foto': self.foto
        }

    @staticmethod
    def validar_auth_token(auth_token):
        "Valida un auth token y devuelve el id de usuario que fue puesto dentro de él"
        payload = jwt.decode(auth_token, app.config.get('JWT_SECRET_KEY'))
        return payload['sub']
