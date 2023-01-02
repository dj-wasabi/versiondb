import time
import json
from bson import json_util

from api.server.logging import logger
from api.v1artifacts.category import Category
from api.v1artifacts.version import Version
from api.v1artifacts.api import mongoCollectionArtifact, mongoCollectionVerions


class Artifact:
    """My Artifact Class."""

    def __init__(self, data: dict = {}) -> None:
        if 'name' in data:
            self.name = data['name']
        if 'category' in data:
            self.category = data['category']
        if 'url' in data:
            self.url = data['url']
        if 'git' in data:
            self.git = data['git']
        if 'metadata' in data:
            self.metadata = data['metadata']
        else:
            self.metadata = []
        if 'created_by' in data:
            self.created_by = data['created_by']
        if 'created_date' in data:
            self.created_date = data['created_date']
        if 'updated_by' in data:
            self.updated_by = data['updated_by']
        if 'updated_date' in data:
            self.updated_date = data['updated_date']
        if 'version' in data:
            self.version = data['version']
        else:
            self.version = "0.0.0"
        logger.debug('We have version "{d}" in init.'.format(d=self.version))


    def search_by_name(self, name: str = None) -> bool:
        artifactFound = mongoCollectionArtifact.count_documents({"name": name})
        if artifactFound == 0:
            return False

        artifactData = mongoCollectionArtifact.find_one({"name": name})
        logger.debug('We have data from artifact: {d}'.format(d=artifactData))
        self.__init__(data=artifactData)
        return True


    def create(self, user: str = None) -> tuple:
        self.created_date = int(time.time())
        self.created_by = user

        if not self.search_by_name(name=self.name):
            data = self._get_json()
            if 'name' not in data or 'category' not in data:
                return {"error": "Both 'name' and 'category' are required."}, 409
            logger.debug("We received the data '{d} to create".format(d=data))
            category = Category()
            if not category.search_by_name(name=data['category']):
                category.create(name=data['category'], user=user)
            category.add_artifact(name=self.name)
            version = Version(data=data)
            version.create(user=user)

            try:
                mongoCollectionArtifact.insert_one(data)
            except Exception as e:
                logger.warning('Error while creating artifact {a}: {e}'.format(a=self.name, e=e))
            return self._get_json(), 201
        else:
            return {"error": "Artifact already exist."}, 409


    def _get_json(self) -> dict:
        return json.loads(json_util.dumps(self.__dict__))


    def get(self) -> dict:
        return self._get_json(), 200


    def getAllVersions(self) -> tuple:
        versions_list = []
        artifactData = mongoCollectionVerions.find({"name": self.name})
        for version in artifactData:
            vDict = {
                "version": version["version"],
                "created": version["created_date"]
            }
            versions_list.append(vDict)

        dataDict = {
            "versions": versions_list
        }
        return dataDict, 200


    def getNextVersion(self, name: str = None, type: str = "patch") -> tuple:
        version = Version()

        if self.search_by_name(name=name):
            logger.info("We have version {v} in artifact.".format(v=self.version))
            version.search_by_name(name=name, version=self.version)
            if type == "patch":
                version.updatePatch()
            elif type == "minor":
                version.updateMinor()
            elif type == "major":
                version.updateMajor()
            data, state = version.get()
            return data, state
        else:
            return {"error": "Version for provided artifact not found."}, 404


    def update(self, name: str = None, user: str = None, type: str = "patch") -> tuple:
        self.updated_date = int(time.time())
        self.updated_by = user
        version = Version()

        if self.search_by_name(name=name):
            logger.info("We have version {v} in artifact.".format(v=self.version))
            version.search_by_name(name=name, version=self.version)

            if type == "patch":
                version.updatePatch()
            elif type == "minor":
                version.updateMinor()
            elif type == "major":
                version.updateMajor()

            data = version.create(user=user)
            self.version = version.version
            logger.debug("We have set version {s} for the 'version'".format(s=self.version))
            self.updateField(field="version")
            return data, 201
        else:
            return {"error": "Version for provided artifact not found."}, 404


    def patch(self, user: str = None, data: str = {}):
        data["updated_date"] = int(time.time())
        data["updated_by"] = user

        for key in data.keys():
            self[key] = data[key]
            self.updateField(field=key)

        self.updateField(field=key)
        newData = self._get_json()
        return newData, 200


    def updateField(self, field: str = None):
        data = self._get_json()
        logger.debug("Found 'data': {s}".format(s=data))
        logger.debug("Input named 'field': {s}".format(s=field))
        query = {"name": self.name}
        update = { "$set": {field: data[field]}}
        try:
            mongoCollectionArtifact.update_one(query, update)
        except Exception as e:
            logger.warning("Error while updating artifact '{n}' with message: {e}".format(n=self.name, e=e))

