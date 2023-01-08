import os
from flask import Flask, Blueprint
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from api.server.config.settings import app_config
from api.server.logging import logger, loggerAudit
from api.server.mongodb.initialise import initialise

authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

app = Flask(__name__)
api = Api(
    title="VersionDB",
    version="1.0",
    description="Application to store 'version' of artifacts and generate a (s)bom.",
    authorizations=authorizations,
)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)



def create_app(config_name, app=app, api=api):
    app.config.from_object(app_config[config_name])

    from api.v1artifacts.views import nsArtifact as nsArtifact
    from api.v1boms.views import nsBom as nsBom
    from api.v1users.views import nsUserManagement as nsUserManagement
    from api.v1groups.views import nsGroupManagement as nsGroupManagement

    api.add_namespace(nsArtifact)
    api.add_namespace(nsBom)
    api.add_namespace(nsUserManagement)
    api.add_namespace(nsGroupManagement)
    initialise()

    # jwt.init_app(app)
    api.init_app(app)
    return app
