import time
import json
from bson import json_util
from api.server.logging import logger

from api.v1categories.category import Category
from api.v1artifacts.api import mongoCollectionVerions


class Version:
    """My Version Class."""

    def __init__(self, data: dict = {}) -> None:
        if 'created_date' in data:
            self.created_date = int(data['created_date'])
        if 'created_by' in data:
            self.created_by = data['created_by']
        if 'updated_date' in data:
            self.updated_date = int(data['updated_date'])
        if 'updated_by' in data:
            self.updated_by = data['updated_by']
        if 'commit' in data:
            self.commit = data['commit']
        if 'name' in data:
            self.name = data['name']
        if 'major' in data:
            self.major = data['major']
        if 'minor' in data:
            self.minor = data['minor']
        if 'patch' in data:
            self.patch = data['patch']
        if 'shasum' in data:
            self.shasum = data['shasum']
        if 'version' in data:
            self.version = data['version']
            self.major = int(data['version'].split('.')[0])
            self.minor = int(data['version'].split('.')[1])
            self.patch = int(data['version'].split('.')[2])
        else:
            self.version = "0.0.0"

    def _removeOutput(self, data: dict = {}) -> dict:
      if "major" in data:
        data.pop("major")
      if "minor" in data:
        data.pop("minor")
      if "patch" in data:
        data.pop("patch")
      if "_id" in data:
        data.pop("_id")
      return data


    def search_by_name(self, name: str = None, version: str = None) -> bool:
        logger.debug("We have version {v} in version.".format(v=version))
        versionFound = mongoCollectionVerions.count_documents({"name": name, "version": version})
        if versionFound == 0:
          logger.debug('No version "{v}" found.'.format(v=version))
          return False

        versionInfo = mongoCollectionVerions.find_one({"name": name, "version": version})
        versionData = json.loads(json_util.dumps(versionInfo))
        logger.debug("We have data {d}.".format(d=version))
        self.__init__(data=versionData)
        return True


    def create(self, user: str = None) -> dict:
        self.created_date = int(time.time())
        self.created_by = user

        data = json.loads(json_util.dumps(self.__dict__))
        logger.debug("Creating version {v} for artifact {a}".format(a=data["name"], v=data["version"]))
        mongoCollectionVerions.insert_one(data)
        return {"version": json.loads(json_util.dumps(self.__dict__['version']))}


    def _get_json(self) -> dict:
        return self._removeOutput(json.loads(json_util.dumps(self.__dict__)))


    def get(self) -> dict:
        return self._get_json(), 200


    def update(self, user: str = None, data: dict = {}) -> tuple:
        self.updated_date = int(time.time())
        self.updated_by = "admin"

        if 'shasum' in data:
            self._set_shasum(value=data["shasum"])
            self.updateField(field="shasum")
        if 'commit' in data:
            self._set_commit(value=data["commit"])
            self.updateField(field="commit")
        self.updateField(field="updated_date")
        self.updateField(field="updated_by")
        newData = self._get_json()
        return newData, 200


    def delete(self):
        logger.warning("Deleting group {g}.".format(g=self.name))
        try:
            query = {"name": self.name, "version": self.version}
            mongoCollectionVerions.delete_one(query)
        except Exception as error:
          logger.warning("Error {e} while deleting version {v}".format(v=self.version, e=error))
          return {"error": "And error {e} occured".format(e=error)}, 400

        if not self.search_by_name(name=self.name):
            return {}, 204
        else:
            return {"error": "Version does not exist."}, 404


    def updateField(self, field: str = None):
        data = self._get_json()
        logger.debug("Found 'data': {s}".format(s=data))
        logger.debug("Input named 'field': {s}".format(s=field))
        query = {"name": self.name, "version": self.version}
        update = { "$set": {field: data[field]}}
        try:
            mongoCollectionVerions.update_one(query, update)
        except Exception as e:
            logger.warning("Error while updating artifact '{n}' with message: {e}".format(n=self.name, e=e))


    def updateVersion(self):
        self.version = "{ma}.{mi}.{p}".format(
            ma=self.major,
            mi=self.minor,
            p=self.patch
        )
        logger.info("Updated version to {v} for artifact {a}.".format(v=self.version, a=self.name))


    def _set_shasum(self, value):
        self.shasum = value


    def _set_commit(self, value):
        self.commit = value


    def updatePatch(self):
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


