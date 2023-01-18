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
        else:
            self.is_active = True
        if 'username' in data:
            self.username = data['username']
        if 'groups' in data:
            self.groups = data['groups']


    def authenticateUser(self, data={}) -> tuple:
        """Authenticate a user"""
        username = data['username']
        password = data['password']

        try:
            passwordCheck = self._validatePassword(username=username, password=password)
            # found = mongoCollectionUser.find_one({"is_active": True, "username": username})
            # logger.debug('Looking for user: {u}'.format(u=username))
            # mongodbData = json.loads(json_util.dumps(found))
            # passwordCheck = myBcrypt.check_password_hash(mongodbData['password'], password)

            if passwordCheck:
                logger.debug('Password check for {u} was successfull'.format(u=username))
                expires = datetime.timedelta(hours=1)
                access_token = create_access_token(identity=str(username), expires_delta=expires)
                logger.debug('We have a successfull authentication for user {u}'.format(u=username))
                return {"token": access_token}, 200
        except Exception as e:
            logger.debug('Authentication failed. Invalid username/password combination for {u}'.format(u=username))
            return {"error": "Authentication failed. Invalid username/password combination"}, 401


    def _validatePassword(self, username: str = None, password: str = None):
        """Validate password for provided user."""
        myBcrypt = Bcrypt()
        found = mongoCollectionUser.find_one({"is_active": True, "username": username})
        logger.debug('Looking for user: {u}'.format(u=username))
        mongodbData = json.loads(json_util.dumps(found))
        return myBcrypt.check_password_hash(mongodbData['password'], password)


    # def changePassword(self, username: str = None, data: dict = {}):
    #     """Change password for user"""
    #     password = data['password']
    #     passwordCheck = self._validatePassword(username=username, password=password)
    #     if passwordCheck:
    #         hashVar = self._encryptPassword(value=password)
    #         query = {"name": self.name}
    #         update = { "$set": {"password": hashVar}}
    #         try:
    #             mongoCollectionUser.update_one(query, update)
    #         except Exception as e:
    #             logger.warning("Error while updating password for user '{n}' with message: {e}".format(n=self.name, e=e))


    def _encryptPassword(self, value: str = None) -> str:
        """Encrypt the password"""
        myBcrypt = Bcrypt()
        return myBcrypt.generate_password_hash(value).decode("utf-8")

    def _get_json(self) -> dict:
        """Return the current object as json."""
        return json.loads(json_util.dumps(self.__dict__))


    def get(self) -> tuple:
        """Return the current object as json, but with status code."""
        return self._get_json(), 200


    def create(self, password: str = None) -> tuple:
        """Create the new user."""
        hashVar = self._encryptPassword(value=password)
        del password
        logger.debug("Encrypting password and remove 'cleartext' from dict.")

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
            del userDict["password"]
            del hashVar
            logger.debug("Create a user with data {a}".format(a=userDict))
            # Add user to the groups
            for group in self.groups:
                myGroup = Group()
                myGroup.search_by_name(name=group)
                myGroup.add_user(username=self.username)
        except Exception as e:
            return {"error": e}, 400
        return self._get_json(), 201


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
        """Check if provided group is already in the configured groups."""
        if group in self.groups:
            return True
        return False


    def add_to_group(self, groupname: str = None):
        """Add a user to a group."""
        try:
            mongoCollectionUser.update_one({'username': self.username}, {'$push': { "groups": groupname } } )
            logger.debug('Added group {g} for user {u}'.format(u=self.username, g=groupname))
            self.groups.append(groupname)
            return self._get_json(), True
        except Exception as e:
          logger.debug("Error while adding group '{g}' to user {u} with error {e}.".format(u=self.username, g=groupname, e=e))
          return {"error": "Error while adding user to group."}, False


    def remove_from_group(self, groupname: str = None):
        """Removes a user from a group."""
        try:
            mongoCollectionUser.update_one({'username': self.username}, { '$pull': { "groups": groupname } } )
            logger.debug("Successfully removed '{u}' from group {g}.".format(g=groupname, u=self.username))
            self.groups.remove(groupname)
            return "", True
        except Exception as e:
            logger.debug("Error while deleting group '{g}' from user {u} with error {e}.".format(u=self.username, g=groupname, e=e))
            return {"error": "Error while remove user from group."}, False
