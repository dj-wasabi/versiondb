from flask_restx import Namespace
from api.server.mongodb.mongodb import db

nsArtifact = Namespace(
  "/api/v1/artifacts",
  path="/api/v1/artifacts",
  version="1.0",
  description="Create and provide artifacts maintenance."
)

mongoCollectionArtifact = db.artifacts
mongoCollectionCategory = db.categories
mongoCollectionVerions = db.versions
