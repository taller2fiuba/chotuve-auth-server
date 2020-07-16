from functools import wraps
from flask import request, g

from app import app
from app.models.app_server import AppServer
from app.generador_token import decodificar_token

def requiere_admin(funcion):
    @wraps(funcion)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '')[len('Bearer '):]
        if not validar_admin_token(token):
            return {'mensaje': 'Token de usuario inválido'}, 401

        g.es_admin = True
        return funcion(*args, **kwargs)
    return decorated_function

def requiere_app_token(funcion):
    @wraps(funcion)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('X-APP-SERVER-TOKEN')
        if not validar_app_token(token):
            return {'mensaje': 'App token inválido'}, 401

        g.es_admin = False
        return funcion(*args, **kwargs)
    return decorated_function

def requiere_app_token_o_admin(funcion):
    @wraps(funcion)
    def decorated_function(*args, **kwargs):
        app_token = request.headers.get('X-APP-SERVER-TOKEN')
        admin_token = request.headers.get('Authorization', '')[len('Bearer '):]

        g.es_admin = validar_admin_token(admin_token)
        if g.es_admin or validar_app_token(app_token):
            return funcion(*args, **kwargs)

        return {}, 401
    return decorated_function

def validar_admin_token(token):
    if not token:
        return False

    data = decodificar_token(token)
    if not data or not data.get('es_admin', False):
        return False

    return True

def validar_app_token(token):
    IGNORAR_APP_SERVER_TOKEN = app.config.get('IGNORAR_APP_SERVER_TOKEN')
    return IGNORAR_APP_SERVER_TOKEN or (token and AppServer.validar_token(token))
