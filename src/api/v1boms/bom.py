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
        self.artifacts = {}


    # def get_current(self, group: str = None) -> dict:
    #     myBom = {}
    #     if group is None:
    #         search = {}
    #     else:
    #         search = {"name": group}

    #     groupsData = self._get_json(data=mongoCollectionGroups.find(search))

    #     for group in groupsData:
    #         name = group["name"]
    #         myBom[name] = {}

    #         artifactData = self._get_json(data=mongoCollectionArtifact.find({"group": name}))
    #         for artifact in artifactData:
    #             artifactName = artifact["name"]
    #             artifactVersion = artifact["version"]
    #             myBom[name][artifactName] = artifactVersion
    #     if len(myBom.items()) == 0:
    #         return {"message": "Group not found."}, 404
    #     return myBom, 200


    def get_latest(self) -> tuple:
        name = self.name
        logger.debug('We have name "{d}" looking for.'.format(d=self.name))
        artifactData = self._get_json(data=mongoCollectionArtifact.find({"group": name}))
        logger.debug('We have artifactData from group: {d}'.format(d=artifactData))

        for artifact in artifactData:
            artifactName = artifact["name"]
            artifactVersion = artifact["version"]
            self.artifacts[artifactName] = artifactVersion
        return self._get_json(), 200


    def search_by_name(self, name: str = None) -> bool:
        if name is None:
            search = {}
        else:
            search = {"name": name}

        mongodbData = mongoCollectionGroups.count_documents(search)
        logger.debug('We have found {d} groups'.format(d=mongodbData))
        if mongodbData  == 0:
            return False

        groupData = mongoCollectionGroups.find_one({"name": name})
        logger.debug('We have data from group: {d}'.format(d=groupData))
        self.__init__(data=groupData)
        return True


    def _get_json(self, data: dict = None) -> dict:
        if data is None:
            logger.debug('Yeah, i am here.')
            data = self.__dict__
        return json.loads(json_util.dumps(data))


    def patchBom(self, user: str = None) -> tuple:
        group = Group()
        if group.search_by_name(name=self.name):
            self._updatePatch()
            group.version = self.version
            group.update(field="version")
            data = self.get_latest()[0]
            data["created_date"] = int(time.time())
            data["created_by"] = user
            _ = mongoCollectionBom.insert_one(data)
            return data, 200
        else:
            return {"message": "Group not found."}, 404

    def updateVersion(self):
        self.version = "{ma}.{mi}.{p}".format(
            ma=self.major,
            mi=self.minor,
            p=self.patch
        )
        logger.info("Updated version to {v} for group {a}.".format(v=self.version, a=self.name))

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
            mongoCollectionGroups.update_one(query, update)
        except Exception as e:
            logger.warning("Error while updating artifact '{n}' with message: {e}".format(n=self.name, e=e))
