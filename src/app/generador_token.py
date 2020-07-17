import datetime
import jwt

from app import app

JWT_SECRET_KEY = app.config.get('JWT_SECRET_KEY')

def generar_token_usuario(uid: int, es_admin: bool) -> str:
    '''
    Genera un token de autenticación para un usuario.
    Devuelve el token generado como cadena.
    '''
    return _generar_token({'uid': uid, 'es_admin': es_admin})

def generar_token_app_server(app_id: int) -> str:
    '''
    Genera un token de autenticación para un App Server.
    Devuelve el token generado como cadena.
    '''
    return _generar_token({'app_id': app_id})

def decodificar_token(token: str):
    '''
    Decodifica un token de autenticación.
    '''
    try:
        return jwt.decode(token, JWT_SECRET_KEY)['sub']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def _generar_token(data):
    return _generar_jwt({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365*10),
        'iat': datetime.datetime.utcnow(),
        'sub': data
    }).decode()

def _generar_jwt(payload):
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
