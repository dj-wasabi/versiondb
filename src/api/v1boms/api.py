from flask_restx import Namespace
from api.server.mongodb.mongodb import db

nsBom = Namespace(
  "/api/v1/boms",
  path="/api/v1/boms",
  version="1.0",
  description="Provide overview of Bill of Materials."
)

mongoCollectionBom = db.boms
