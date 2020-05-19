#!/usr/bin/env python3
#pylint: skip-file

import os

def blow(envvar):
    '''
    Lanza una excepción indicando que una variable de entorno requerida no esta
    configurada o tiene un valor incorrecto.
    '''
    valor = os.environ.get(envvar)
    raise ValueError(f'La variable de entorno {envvar} tiene un ' +
                     'valor incorrecto: ' + repr(valor))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or blow('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'JWT_SECRET_KEY'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
