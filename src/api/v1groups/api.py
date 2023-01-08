from flask_restx import Namespace
from api.server.mongodb.mongodb import db

nsGroupManagement = Namespace(
  "/api/v1/groups",
  path="/api/v1/groups",
  version="1.0",
  description="(User) Groups Management"
)

mongoCollectionUserGroups = db.groups
