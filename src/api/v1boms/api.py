from flask_restx import Api
from api.server.mongodb.mongodb import db

api = Api(version='1.0', title='VersionDB', description='VersionDB')
nsBom = api.namespace('api/v1/boms', description='Provide overview of Bill of Materials.')

mongoCollectionBom = db.boms
