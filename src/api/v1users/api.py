from flask_restx import Namespace
from api.server.mongodb.mongodb import db

nsUserManagement = Namespace(
  "/api/v1/users",
  path="/api/v1/users",
  version="1.0",
  description="User Management"
)

mongoCollectionUser = db.users
mongoCollectionUserGroups = db.groups
