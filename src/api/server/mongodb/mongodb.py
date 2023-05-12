from pymongo import MongoClient
import mongomock
from api.server.mongodb import getMongoConfig
from api.server.config import getConfig


configSettings = getMongoConfig()
flaskEnv = getConfig(name="VERSIONDB_ENVIRONMENT")

if flaskEnv == "ci":
  client = mongomock.MongoClient()
else:
  client = MongoClient(**configSettings)

flask_db = getConfig(name="VERSIONDB_MONGODB_DATABASE") 
db = client[flask_db]
