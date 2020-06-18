from functools import wraps
from flask import make_response

def habilitar_cors(funcion, *dominios):
    if len(dominios) == 0:
        dominios = ('*',)

    @wraps(funcion)
    def funcion_decorada(*args, **kwargs):
        respuesta = make_response(funcion(*args, **kwargs))
        respuesta.headers['Access-Control-Allow-Origin'] = ','.join(dominios)
        return respuesta
    return funcion_decorada
        