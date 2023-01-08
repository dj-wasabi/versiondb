import time
import json
from api.v1artifacts.category import Category
from bson import json_util

from api.v1artifacts.api import mongoCollectionCategory, mongoCollectionArtifact
from api.v1boms.api import mongoCollectionBom
from api.server.logging import logger


class Bom:
    """My Bom Class."""

    def __init__(self, data: dict = {}) -> None:
        if 'name' in data:
            self.name = data['name']
        else:
            self.name = None
        if 'tmp_artifacts' in data:
            self.tmp_artifacts = data['tmp_artifacts']
        else:
            self.tmp_artifacts = []
        if 'artifacts' in data:
            self.artifacts = data['artifacts']
        else:
            self.artifacts = {}
        if 'version' in data:
            self.version = data['version']
            self.major = int(data['version'].split('.')[0])
            self.minor = int(data['version'].split('.')[1])
            self.patch = int(data['version'].split('.')[2])
        else:
            self.version = "0.0.0"
        if 'major' in data:
            self.major = data['major']
        if 'minor' in data:
            self.minor = data['minor']
        if 'patch' in data:
            self.patch = data['patch']
        if 'created_by' in data:
            self.created_by = data['created_by']
        if 'created_date' in data:
            self.created_date = data['created_date']
        if 'updated_by' in data:
            self.updated_by = data['updated_by']
        if 'updated_date' in data:
            self.updated_date = data['updated_date']


    def get_latest(self) -> tuple:
        name = self.name
        logger.debug('We have name "{d}" looking for.'.format(d=self.name))

        for artifact in self.tmp_artifacts:
            artifactData = mongoCollectionArtifact.find_one({"name": artifact})
            logger.debug('We have artifactData: {a}'.format(a=artifactData))
            artifactName = artifactData["name"]
            artifactVersion = artifactData["version"]
            self.artifacts[artifactName] = artifactVersion
        return self._get_json(), 200


    def search_by_name(self, name: str = None) -> bool:
        if name is None:
            search = {}
        else:
            search = {"name": name}

        mongodbData = mongoCollectionCategory.count_documents(search)
        logger.debug('We have found {d} category'.format(d=mongodbData))
        if mongodbData  == 0:
            return False

        CategoryData = mongoCollectionCategory.find_one(search)
        logger.debug('We have data from category: {d}'.format(d=CategoryData))
        # This is now a list, but we have to store it in a different key
        CategoryData["tmp_artifacts"] = CategoryData["artifacts"]
        del CategoryData["artifacts"]
        self.__init__(data=CategoryData)
        return True


    def _get_json(self, data: dict = None) -> dict:
        if data is None:
            data = self.__dict__
            logger.debug('Yeah, i am here: {d}'.format(d=data))
        # return self._removeOutput(data=json.loads(json_util.dumps(data)))
        return data


    def _removeOutput(self, data: dict = {}) -> dict:
      if "major" in data:
        data.pop("major")
      if "minor" in data:
        data.pop("minor")
      if "patch" in data:
        data.pop("patch")
      if "tmp_artifacts" in data:
        data.pop("tmp_artifacts")
      if "_id" in data:
        data.pop("_id")
      return data


    def minorBom(self, user: str = None) -> tuple:
        category = Category()
        if category.search_by_name(name=self.name):
            self._updateMinor()
            category.version = self.version
            category.update(field="version")
            data = self.get_latest()[0]
            data["created_date"] = int(time.time())
            data["created_by"] = user
            del data["tmp_artifacts"]
            _ = mongoCollectionBom.insert_one(data)
            logger.debug('We have bom data: {d}'.format(d=data))
            return self._removeOutput(data=data), 200
        else:
            return {"error": "Category not found."}, 404


    def patchBom(self, user: str = None) -> tuple:
        category = Category()
        if category.search_by_name(name=self.name):
            self._updatePatch()
            logger.debug('Updating version 1...')
            category.version = self.version
            logger.debug('Check if we are here21212 ..')
            category.update(field="version")
            logger.debug('Updating version...')
            data = self.get_latest()[0]
            data["created_date"] = int(time.time())
            data["created_by"] = user
            del data["tmp_artifacts"]
            mongoCollectionBom.insert_one(data)
            logger.debug('We have data: {d}'.format(d=data))
            return self._removeOutput(data=data), 200
        else:
            return {"message": "Category not found."}, 404

    def updateVersion(self):
        self.version = "{ma}.{mi}.{p}".format(
            ma=self.major,
            mi=self.minor,
            p=self.patch
        )
        logger.info("Updated version to {v} for Category {a}.".format(v=self.version, a=self.name))

    def _updatePatch(self):
        self.patch += 1
        self.updateVersion()

    def updateMinor(self):
        self.patch = 1
        self.minor += 1
        self.updateVersion()

    def updateMajor(self):
        self.patch = 1
        self.minor = 0
        self.major += 1
        self.updateVersion()




    def _update(self, field: str = None):
        data = self._get_json()
        query = {"name": self.name}
        update = { "$set": {field: data[field]}}
        try:
            mongoCollectionCategory.update_one(query, update)
        except Exception as e:
            logger.warning("Error while updating artifact '{n}' with message: {e}".format(n=self.name, e=e))
