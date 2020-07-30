import datetime

from sqlalchemy import func
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
    fecha = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Usuario {self.email}>'

    def __init__(self, email, password):
        self.email = email
        self.registro_fecha_hora = datetime.datetime.now()
        self.actualizar_clave(password)

    def actualizar_clave(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

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
        if not data:
            return None
        usuario_id = data.get('uid')
        es_admin = data.get('es_admin')

        if usuario_id == 0 and es_admin:
            return (None, True)

        usuario = Usuario.query.filter_by(id=usuario_id).one_or_none()
        if not usuario or not usuario.habilitado:
            return None
        return (usuario, False)

    @staticmethod
    def cantidad_usuarios():
        return Usuario.query.count()

    @staticmethod
    def usuarios_por_fecha(f_inicio, f_final):
        f_final = f_final + datetime.timedelta(seconds=59, minutes=59, hours=23)
        #este es ya que sino la query se hara para la f_final
        #a las 00 y no entraran los usuarios de f_final
        query = db.session.query(db.func.date(Usuario.fecha), db.func.count('*')).\
                                 filter(Usuario.fecha >= f_inicio, Usuario.fecha <= f_final).\
                                 group_by(db.func.date(Usuario.fecha)).all()
        usuarios = {}
        for fecha in query:
            usuarios[str(fecha[0])] = fecha[1]

        #saco los segundos y minutos
        fecha = datetime.date(f_inicio.year, f_inicio.month, f_inicio.day)
        f_final = datetime.date(f_final.year, f_final.month, f_final.day)
        while fecha <= f_final:
            if str(fecha) not in usuarios:
                usuarios[str(fecha)] = 0
            fecha = fecha + datetime.timedelta(days=1)
        return usuarios
