from app.models.usuario import Usuario
from app import db

def cargar_usuario(**kwargs):
    if "usuario_id" in kwargs:
        return Usuario.query.filter_by(id=kwargs["usuario_id"]).first()
    if "mail" in kwargs:
        return Usuario.query.filter_by(email=kwargs["mail"]).first()
    return None

def usuario_existente(**kwargs):
    if "usuario_id" in kwargs:
        usuario = cargar_usuario(usuario_id=kwargs["usuario_id"])
    elif "mail" in kwargs:
        usuario = cargar_usuario(mail=kwargs["mail"])
    else:
        return False
    if not usuario:
        return False
    return  True

def crear_usuario(correo, password):
    return Usuario(email=correo, password=password)

def guardar_usuario(usuario):
    db.session.add(usuario)
    db.session.commit()
