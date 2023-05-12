import time
import json
from bson import json_util

from api.v1artifacts.api import mongoCollectionCategory
from api.server.logging import logger


class Category:
    """My DB Class."""

    def __init__(self, data: dict = {}):
        """Init."""
        if 'name' in data:
            self.name = data['name']
        else:
            self.name = None
        if 'read' in data:
            self.read = data['read']
        if 'write' in data:
            self.write = data['write']
        if 'admin' in data:
            self.admin = data['admin']
        if 'artifacts' in data:
            self.artifacts = data['artifacts']
        else:
            self.artifacts = []
        if 'created_by' in data:
            self.created_by = data['created_by']
        if 'created_date' in data:
            self.created_date = data['created_date']
        if 'updated_by' in data:
            self.updated_by = data['updated_by']
        if 'updated_date' in data:
            self.updated_date = data['updated_date']


    def create(self, user: str = None) -> bool:
        self.created_date = int(time.time())
        self.created_by = user

        if not self.search_by_name(name=self.name):
            categoryData = self._get_json()
            try:
                mongoCollectionCategory.insert_one(categoryData)
                logger.info("Created catagory '{g}.".format(g=self.name))
            except Exception as e:
                logger.error("Error while creating catagory '{e}.".format(e=e))
                return {"error": "Error while creating catagory"}, 200
            return self._get_json(), 201
        else:
            return {"error": "Category already exist."}, 409


    def get(self):
        return self._get_json(), 200


    def get_all(self) -> tuple:
        allCategories = []
        try:
            findAllCategories = mongoCollectionCategory.find({})
            for category in findAllCategories:
                categoryData = json.loads(json_util.dumps(category))
                minimisedData = {
                    "name": categoryData['name'],
                    "artifacts": categoryData['artifacts']
                }
                allCategories.append(minimisedData)
            return allCategories, 200
        except:
            return {"error": "Error while getting the data"}, 200


    def search_by_name(self, name: str = None) -> bool:
        mongodbData = mongoCollectionCategory.count_documents({"name": name})
        if mongodbData == 0:
            return False

        groupData = mongoCollectionCategory.find_one({"name": name})
        logger.debug('We have data from group: {d}'.format(d=groupData))
        self.__init__(data=groupData)
        return True


    def add_artifact(self, name: str = None, user: str = None):
        """Add an artifact to the category, used by the artifacts class."""
        self.updated_date = int(time.time())
        self.updated_by = user

        artifacts = self.artifacts
        if name not in artifacts:
            artifacts.append(name)
            self._updateField(field="artifacts")


    def remove_artifact(self, name: str = None, user: str = None) -> bool:
        """Remove an artifact from the category, used by the artifacts class."""
        self.updated_date = int(time.time())
        self.updated_by = user
        artifacts = self.artifacts
        if name in artifacts:
            artifacts.pop(name)
            self._updateField(field="artifacts")
            return True
        else:
            return False


    def delete(self):
        logger.warning("Deleting category {g}.".format(g=self.name))
        try:
            myquery = { "name": self.name }
            mongoCollectionCategory.delete_one(myquery)
        except Exception as error:
          logger.warning("Error {e} while deleting category {g}".format(g=self.name, e=error))
          return {"error": "And error {e} occured".format(e=error)}, 400

        if not self.search_by_name(name=self.name):
            return {}, 204
        else:
            return {"error": "Category not found."}, 404


    def _get_json(self) -> dict:
        return json.loads(json_util.dumps(self.__dict__))


    def _updateField(self, field: str = None):
        data = self._get_json()
        query = {"name": self.name}
        update = { "$set": {field: data[field]}}
        try:
            mongoCollectionCategory.update_one(query, update)
        except Exception as e:
            logger.warning("Error while updating group '{n}' with message: {e}".format(n=self.name, e=e))
