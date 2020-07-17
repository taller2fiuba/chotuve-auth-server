#!/usr/bin/env python3
#pylint: skip-file

import os
from logging.config import dictConfig

def blow(envvar):
    '''
    Lanza una excepción indicando que una variable de entorno requerida no esta
    configurada o tiene un valor incorrecto.
    '''
    valor = os.environ.get(envvar)
    raise ValueError(f'La variable de entorno {envvar} tiene un ' +
                     'valor incorrecto: ' + repr(valor))

def configurar_logger():
    dictConfig(dict(
        version=1,
        disable_existing_loggers=False,
        formatters={
            "default": {"format": "%(levelname)s en %(module)s: %(message)s"},
        },
        handlers={
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        root={"handlers": ["console"], "level": "INFO"},
    ))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or blow('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'JWT_SECRET_KEY'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    IGNORAR_APP_SERVER_TOKEN = os.environ.get('IGNORAR_APP_SERVER_TOKEN') or False
    ADMIN_EMAIL = os.environ.get('CHOTUVE_AUTH_ADMIN_EMAIL') or 'admin'
    ADMIN_CLAVE = os.environ.get('CHOTUVE_AUTH_ADMIN_CLAVE') or 'admin'
    APP_VERSION = "0.0.1"
