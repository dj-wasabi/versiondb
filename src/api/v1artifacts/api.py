from flask_restx import Api
from api.server.mongodb.mongodb import db

api = Api(version='1.0', title='VersionDB', description='VersionDB')
nsArtifact = api.namespace('api/v1/artifacts', description='Create and provide artifacts maintenance.')

mongoCollectionArtifact = db.artifacts
mongoCollectionCategory = db.categories
mongoCollectionVerions = db.versions
