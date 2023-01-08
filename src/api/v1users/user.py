import time
import datetime
import json
from flask_bcrypt import Bcrypt
from bson import json_util
from flask_jwt_extended import create_access_token

from api.server.logging import logger
from api.v1users.api import mongoCollectionUser
from api.v1groups.group import Group


class User:
    """My User Class."""

    def __init__(self, data: dict = {}) -> None:
      if 'created_date' in data:
          self.created_date = data['created_date']
      if 'is_active' in data:
          self.is_active = data['is_active']
      if 'username' in data:
          self.username = data['username']
      if 'groups' in data:
          self.groups = data['groups']


    def authenticateUser(self, data={}) -> tuple:
      username = data['username']
      password = data['password']
      myBcrypt = Bcrypt()

      try:
        found = mongoCollectionUser.find_one({"is_active": True, "username": username})
        logger.debug('Looking for user: {u}'.format(u=username))
        mongodbData = json.loads(json_util.dumps(found))
        passwordCheck = myBcrypt.check_password_hash(mongodbData['password'], password)

        if passwordCheck:
          logger.debug('Password check for {u} was successfull'.format(u=username))
          expires = datetime.timedelta(hours=1)
          access_token = create_access_token(identity=str(username), expires_delta=expires)
          logger.debug('We have a successfull authentication for user {u}'.format(u=username))
          return {"token": access_token}, 200
      except Exception as e:
        logger.debug('Password check for {u} was unsuccessfull'.format(u=username))
        return {"error": "Authentication failed. Invalid username/password combination"}, 401


    def _encryptPassword(self, value: str = None) -> str:
      myBcrypt = Bcrypt()
      return myBcrypt.generate_password_hash(value).decode("utf-8")


    def userExist(self, name: str = None) -> bool:
      userFound = mongoCollectionUser.count_documents({"username": name})
      if userFound == 1:
        return True
      else:
        return False


    def _get_json(self) -> dict:
        return json.loads(json_util.dumps(self.__dict__))


    def get(self) -> tuple:
        return self._get_json(), 200


    def create(self, data={}):
      self.username = data["username"]
      password = data["password"]
      if 'is_active' in data:
        self.is_active = data['is_active']
      else:
        self.is_active = True
        data['is_active'] = True
      if 'groups' in data:
        self.groups = data["groups"]
      else:
        return {"error": "No groups provided for user."}, 400

      hashVar = self._encryptPassword(value=password)
      del password
      userFound = self.userExist(name=self.username)
      if userFound:
        return {"error": "Username is already used."}, 409

      allGroups = Group()
      notExist, state = allGroups.validateGroups(groups=self.groups)
      if not state:
        return {"error": "The groups {l} doesn't exist".format(l=notExist)}, 409

      try:
        userDict = {
          "created_date": int(time.time()),
          "is_active": self.is_active,
          "username": self.username,
          "password": hashVar,
          "groups": self.groups
        }
        mongoCollectionUser.insert_one(userDict)
        for group in self.groups:
          myGroup = Group()
          myGroup.search_by_name(name=group)
          myGroup.add_user(username=self.username)
      except Exception as e:
        return {"error": e}, 400
      return self._removeOutput(data=userDict), 201


    def _removeOutput(self, data: dict = {}) -> dict:
      if "password" in data:
        data.pop("password")
      if "_id" in data:
        data.pop("_id")
      return data


    def search_by_name(self, name: str = None) -> bool:
        userFound = mongoCollectionUser.count_documents({"username": name})
        if userFound == 0:
          logger.debug('No user "{n}" found.'.format(n=name))
          return False

        userData = mongoCollectionUser.find_one({"username": name})
        logger.debug('We have data from user: {d}'.format(d=userData))
        self.__init__(data=userData)
        return True


    def is_in_group(self, group: str = None) -> bool:
        if group in self.groups:
            return True
        return False


    def add_to_group(self, groupname: str = None):
        try:
            mongoCollectionUser.update_one({'username': self.username}, {'$push': { "groups": groupname } } )
            logger.debug('Added group {g} for user {u}'.format(u=self.username, g=groupname))
            self.groups.append(groupname)
            return self._get_json(), True
        except Exception as e:
          logger.debug("Error while adding group '{g}' to user {u} with error {e}.".format(u=self.username, g=groupname, e=e))
          return {"error": "Error while adding user to group."}, False


    def remove_from_group(self, groupname: str = None):
        try:
          mongoCollectionUser.update_one({'username': self.username}, { '$pull': { "groups": groupname } } )
          logger.debug("Successfully removed '{u}' from group {g}.".format(g=groupname, u=self.username))
          self.groups.remove(groupname)
          return "", True
        except Exception as e:
          logger.debug("Error while deleting group '{g}' from user {u} with error {e}.".format(u=self.username, g=groupname, e=e))
          return {"error": "Error while remove user from group."}, False
