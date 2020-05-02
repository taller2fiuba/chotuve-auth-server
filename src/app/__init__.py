#pylint: skip-file
from flask import Flask
from flask_restful import Resource, Api
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
API = Api(app)


class Ping(Resource):
    def get(self):
        return {}


API.add_resource(Ping, '/ping')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

from app import models
