from functools import wraps
from flask import request

from app.generador_token import decodificar_token

def requiere_admin(funcion):
    @wraps(funcion)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '')[len('Bearer '):]
        if not token:
            return {}, 401

        data = decodificar_token(token)
        if not data or not data.get('es_admin', False):
            return {}, 401

        return funcion(*args, **kwargs)
    return decorated_function
