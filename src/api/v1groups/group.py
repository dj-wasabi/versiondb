import time
import json
from flask_bcrypt import Bcrypt
from bson import json_util

from api.server.logging import logger
from api.v1groups.api import mongoCollectionUserGroups


class Group:
    """My Group Class."""

    def __init__(self, data: str = {}) -> None:
        if 'created_date' in data:
            self.name = data['created_date']
        if 'name' in data:
            self.name = data['name']
        if 'users' in data:
            self.users = data['users']


    def _get_json(self) -> dict:
        return json.loads(json_util.dumps(self.__dict__))


    def get(self) -> tuple:
        return self._get_json(), 200


    def groupExist(self, name: str = None) -> bool:
        groupFound = mongoCollectionUserGroups.count_documents({"name": name})
        if groupFound == 1:
            return True
        else:
            return False

    def validateGroups(self, groups: list = []) -> tuple:
        notExist = []
        for group in groups:
            if not self.groupExist(name=group):
                notExist.append(group)
        if len(notExist) == 0:
            return [], True
        else:
            return notExist, False


    def search_by_name(self, name: str = None) -> bool:
        groupFound = mongoCollectionUserGroups.count_documents({"name": name})
        logger.debug('We have found a group with the name {n} ({s})'.format(n=name, s=groupFound))
        if groupFound == 0:
            return False

        groupData = mongoCollectionUserGroups.find_one({"name": name})
        logger.debug('We have data from group: {d}'.format(d=groupData))
        self.__init__(data=groupData)
        return True


    def add_user(self, username: str = None) -> tuple:
        try:
            mongoCollectionUserGroups.update_one({'name': self.name}, {'$push': {'users': username}})
            logger.info("Added user '{u}' to group {g}.".format(g=self.name, u=username))
            return {"message": "Added user to the group."}, True
        except Exception as e:
          logger.error("Error while adding user '{u}' to group {g} with error {e}.".format(g=self.name, u=username, e=e))
          return {"error": "Error while adding user to group: {e}".format(e=e)}, False


    def is_in_group(self, username: str = None) -> bool:
        if username in self.users:
            return False
        return True


    def remove_user(self, username: str = None):
        try:
          mongoCollectionUserGroups.update_one({'name': self.name}, { '$pull': { "users": username } } )
          logger.info("Successfully removed '{u}' from group {g}.".format(g=self.name, u=username))
          return "", True
        except Exception as e:
          logger.warning("Error while deleting user '{u}' from group {g} with error {e}.".format(g=self.name, u=username, e=e))
          return {"error": "Error while remove user from group."}, False


    def create(self, data: dict = {}):
        self.name = data['name']
        if 'users' in data:
            self.users = data["groups"]
        else:
            self.users = []
        self.created_date = int(time.time())
        myGroup = {
          "created_date": self.created_date,
          "name": self.name,
          "users": self.users
        }
        if self.search_by_name(name=self.name):
            return {"error": "The group already exist."}, 409
        try:
          logger.warning("We have a myDict before {g}.".format(g=myGroup))
          mongoCollectionUserGroups.insert_one(myGroup)
          logger.warning("Created group {g}".format(g=self.name))
        except Exception as error:
          logger.warning("Error {e} while creating group {g}".format(g=self.name, e=error))
          return {"error": "And error {e} occured".format(e=error)}, 400
        return self._get_json(), 201


    def delete(self):
        logger.warning("Deleting group {g}.".format(g=self.name))
        try:
            myquery = { "name": self.name }
            mongoCollectionUserGroups.delete_one(myquery)
        except Exception as error:
          logger.warning("Error {e} while deleting group {g}".format(g=self.name, e=error))
          return {"error": "And error {e} occured".format(e=error)}, 400

        if not self.search_by_name(name=self.name):
            return {}, 204
        else:
            return {"error": "Group does not exist."}, 404
