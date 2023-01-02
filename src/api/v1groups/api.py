from flask_restx import Api
from api.server.mongodb.mongodb import db

api = Api(version='1.0', title='VersionDB', description='VersionDB')
nsGroupManagement = api.namespace('api/v1/groups', description='(User) Groups Management')

mongoCollectionUserGroups = db.groups
