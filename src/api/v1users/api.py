from flask_restx import Api
from api.server.mongodb.mongodb import db

api = Api(version='1.0', title='VersionDB', description='VersionDB')
nsUserManagement = api.namespace('api/v1/users', description='User Management')

mongoCollectionUser = db.users
mongoCollectionUserGroups = db.groups
