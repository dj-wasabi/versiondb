import os
from flask import Flask, Blueprint
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from api.server.config.settings import app_config
from api.server.logging import logger, loggerAudit
from api.server.mongodb.initialise import initialise
from api.v1artifacts.views import nsArtifact as nsArtifact
from api.v1boms.views import nsBom as nsBom
from api.v1users.views import nsUserManagement as nsUserManagement
from api.v1groups.views import nsGroupManagement as nsGroupManagement


app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


def create_app(config_name, app=app, api=api):
    app.config.from_object(app_config[config_name])
    blueprint = Blueprint(config_name, __name__, url_prefix='/')
    api.init_app(blueprint)
    api.add_namespace(nsArtifact)
    api.add_namespace(nsBom)
    api.add_namespace(nsUserManagement)
    api.add_namespace(nsGroupManagement)
    initialise()
    app.register_blueprint(blueprint)

    jwt.init_app(app)
    return app
