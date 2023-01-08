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
        if 'version' in data:
            self.version = data['version']
        else:
            self.version = "0.0.0"
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

    def _get_json(self) -> dict:
        return json.loads(json_util.dumps(self.__dict__))


    def create(self, name: str = None, user: str = None) -> bool:
        self.created_date = int(time.time())
        self.created_by = user
        self.name = name

        myDict = self._get_json()
        try:
            mongoCollectionCategory.insert_one(myDict)
            logger.info("Created group '{g}.".format(g=self.name))
        except Exception as e:
            logger.error("Error while creating group '{e}.".format(e=e))
            return False
        return True


    def search_by_name(self, name: str = None) -> bool:
        mongodbData = mongoCollectionCategory.count_documents({"name": name})
        if mongodbData  == 0:
            return False

        groupData = mongoCollectionCategory.find_one({"name": name})
        logger.debug('We have data from group: {d}'.format(d=groupData))
        self.__init__(data=groupData)
        return True


    def add_artifact(self, name: str = None, user: str = None):
        """Add an artifact to the category."""
        self.updated_date = int(time.time())
        self.updated_by = user

        artifacts = self.artifacts
        if name not in artifacts:
            artifacts.append(name)
            self.updateField(field="artifacts")


    def remove_artifact(self, name: str = None, user: str = None) -> bool:
        """Remove an artifact from the category."""
        self.updated_date = int(time.time())
        self.updated_by = user
        artifacts = self.artifacts
        if name in artifacts:
            artifacts.pop(name)
            self.updateField(field="artifacts")
            return True
        else:
            return False



    def updateField(self, field: str = None):
        data = self._get_json()
        query = {"name": self.name}
        update = { "$set": {field: data[field]}}
        try:
            mongoCollectionCategory.update_one(query, update)
        except Exception as e:
            logger.warning("Error while updating group '{n}' with message: {e}".format(n=self.name, e=e))
