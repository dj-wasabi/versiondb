from flask_restx import Namespace
from api.server.mongodb.mongodb import db

nsCategory = Namespace(
  "/api/v1/categories",
  path="/api/v1/categories",
  version="1.0",
  description="Maintenance of categories. This is basically a group or collection of artifacts."
)

mongoCollectionCategory = db.categories
