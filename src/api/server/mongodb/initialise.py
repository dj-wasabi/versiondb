from api.server.logging import logger
from api.server.mongodb.mongodb import db
from api.server.config import getConfig
from api.v1groups.group import Group
from api.v1users.user import User


def initialise():
  userName = getConfig(name="VERSIONDB_ADMIN_USERNAME")
  userDict = {
    "username": userName,
    "password": getConfig(name="VERSIONDB_ADMIN_PASSWORD"),
    "groups": ["admin"]
  }
  groupDict = {
    "name": "admin"
  }

  # Make sure we have Indexes created/configured
  createIndexes()

  # Create 'admin' user
  adminUser = User(data=userDict)
  adminGroup = Group()
  logger.debug("Creating the admin group '{g}'.".format(g=adminGroup))
  _, _ = adminGroup.create(data=groupDict)
  logger.debug("Creating the admin user '{u}'.".format(u=userName))
  message, _ = adminUser.create(password=userDict["password"])
  logger.debug("User created with '{m}'.".format(m=message))


def createIndex(mongodb: object = None, name: str = None, collection: str = None, fields: list = [], unique: bool = False):
  logger.debug("Create index '{i}' on '{c}'.".format(i=name, c=collection))
  mongodb.create_index(fields, name=name, unique=unique)



def deleteIndex(mongodb: object = None, name: str = None, collection: str = None):
  logger.debug("Deleting index '{i}' on '{c}'.".format(i=name, c=collection))
  mongodb.drop_index(name)



def createIndexes():
  """We will check if there is an index already configured, if not we create one.
  """
  
  index_setup = [
    {
      "name": "users_username_unique",
      "collection": "users",
      # "fields": [("username", 1), ("password", 1)],
      "fields": [("username", 1)],
      "enabled": True,
      "unique": True
    }
  ]

  # Looping thru all 'needed' indexes
  for index in index_setup:
    mongodb = db
    collection = index["collection"]
    mongodb_coll = mongodb[collection]


    index_name = index['name']
    index_fields = index['fields']
    index_enabled = index['enabled']
    index_unique = index['unique']

    indexes = mongodb_coll.index_information()
    logger.debug("Overview indexes in collection '{c}': {s}".format(c=collection, s=indexes))

    if index_name in indexes and not index_enabled:
      # We have an index which we need to delete.
      deleteIndex(mongodb=mongodb_coll, name=index_name, collection=collection)
    elif index_name in indexes and index_enabled:
      # We have the index and it is enabled. Maybe it has changed?
      current_index_config = indexes[index_name]['key']

      if 'unique' in indexes[index_name]:
        current_index_config_unique = indexes[index_name]['unique']
      else:
        current_index_config_unique = False

      if current_index_config != index_fields or index_unique != current_index_config_unique:
        logger.debug("We are not compatible and delete the old index.")
        deleteIndex(mongodb=mongodb_coll, name=index_name, collection=collection)
        createIndex(
          mongodb=mongodb_coll, name=index_name,
          collection=collection, fields=index_fields,
          unique=index_unique
        )
    elif index_name not in indexes and index_enabled:
      # We don't have the index, but we really want it.
      createIndex(
        mongodb=mongodb_coll, name=index_name,
        collection=collection, fields=index_fields,
        unique=index_unique
      )
