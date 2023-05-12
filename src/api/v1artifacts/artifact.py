import time
import json
from bson import json_util

from api.server.logging import logger
from api.v1categories.category import Category
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


    def search_by_name(self, name: str = None) -> bool:
        artifactFound = mongoCollectionArtifact.count_documents({"name": name})
        if artifactFound == 0:
            logger.debug("We did not found artifact with name '{a}'".format(a=name))
            return False

        artifactData = mongoCollectionArtifact.find_one({"name": name})
        logger.debug("We initialise the class with the artifact data.")
        self.__init__(data=artifactData)
        return True


    def _add_to_category(self, category: str = None, user: str = None):
        """Add the artifact to an category. If category does not exist, we create one."""
        categoryObject = Category()
        if not categoryObject.search_by_name(name=category):
            categoryObject = Category({"name": category})
            categoryObject.create(user=user)
        categoryObject.add_artifact(name=self.name)


    def create(self, user: str = None) -> tuple:
        self.created_date = int(time.time())
        self.created_by = user

        if not self.search_by_name(name=self.name):
            data = self._get_json()
            if 'name' not in data or 'category' not in data:
                return {"error": "Both 'name' and 'category' are required."}, 409

            logger.debug("We received the data '{d} to create".format(d=data))
            self._add_to_category(category=data['category'], user=user)
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
        self._set_update_info(user=user)
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
            self._updateField(field="version")
            return data, 201
        else:
            return {"error": "Version for provided artifact not found."}, 404

    def _set_update_info(self, user: str = None):
        self.updated_date = int(time.time())
        self.updated_by = user


    def patch(self, user: str = None, data: str = {}):
        for key in data.keys():
            if 'url' == key:
                self._set_url(value=data['url'])
            elif 'git' == key:
                self._set_git(value=data['git'])
            elif 'metadata' == key:
                self._set_metadata(value=data['metadata'])
            elif 'version' == key:
                self._set_version(value=data['version'], user=user)
            elif 'category' == key:
                self._set_category(value=data['category'], user=user)
            logger.debug('Updating key: {a}'.format(a=key))
            self._updateField(field=key)
        self._set_update_info(user=user)
        return self._get_json(), 200

    def _set_url(self, value: str = None):
        self.url = value
 
    def _set_git(self, value: str = None):
        self.git = value
 
    def _set_metadata(self, value: dict = {}):
        self.metadata = value
 
    def _set_category(self, value: str = None, user: str = None):
        if value != self.category:
            newCategory = Category()
            if not newCategory.search_by_name(name=value):
                newCategory.create(name=value, user=user)
            newCategory.add_artifact(name=self.name, user=user)
            newCategory.remove_artifact(name=self.name, user=user)
 
    def _set_version(self, value: str = None, user: str = None):
        if self.version != value:
            versionData = {
                "name": self.name,
                "version": value
            }
            newVersion = Version(data=versionData)
            newVersion.create(user=user)
        self.version = value

    def _updateField(self, field: str = None):
        data = self._get_json()
        logger.debug("Found 'data': {s}".format(s=data))
        logger.debug("Input named 'field': {s}".format(s=field))
        query = {"name": self.name}
        update = { "$set": {field: data[field]}}
        try:
            mongoCollectionArtifact.update_one(query, update)
        except Exception as e:
            logger.warning("Error while updating artifact '{n}' with message: {e}".format(n=self.name, e=e))

