import datetime

from app import db, bcrypt, generador_token

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=True)
    apellido = db.Column(db.String(255), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(255), nullable=True)
    foto = db.Column(db.String(255), nullable=True)
    habilitado = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.email}>'

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.registro_fecha_hora = datetime.datetime.now()

    def verificar_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generar_auth_token(self):
        return generador_token.generar_token_usuario(self.id, False)

    def serializar(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'direccion' : self.direccion,
            'telefono': self.telefono,
            'foto': self.foto,
            'habilitado': self.habilitado
        }

    @staticmethod
    def validar_auth_token(auth_token):
        """
        Valida un auth token. Si el token es válido y el usuario está
        habilitado, devuelve al usuario correspondiente y un booleano indicando
        si es administrador o no en una tupla (uid, es_admin).
        En caso contrario devuelve None.
        """
        data = generador_token.decodificar_token(auth_token)
        usuario_id = data.get('uid')
        es_admin = data.get('es_admin')

        if usuario_id == 0 and es_admin:
            return (None, True)

        usuario = Usuario.query.filter_by(id=usuario_id).one_or_none()
        if not usuario or not usuario.habilitado:
            return None
        return (usuario, False)
