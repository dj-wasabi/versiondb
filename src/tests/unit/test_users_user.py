import sys
import os
import pytest


currentPath = os.path.dirname(os.path.realpath(__file__))
rootPath = os.path.join(currentPath, "../..")
sys.path.append(rootPath)

from api.v1groups.group import Group
from api.v1users.user import User


def test_api_v1users_search_by_name_not_exist():
    myUser = User()
    assert not myUser.search_by_name(name="dummy")


def test_api_v1users_create():
    groupDict = {
      "name": "mygroupname"
    }
    UserDict = {
      "username": "myusername",
      "password": "mypassword",
      "groups": ["mygroupname"]
    }
    myGroup = Group()
    myGroup.create(data=groupDict)

    myUser = User(data=UserDict)
    output, state = myUser.create(password="mypassword")

    assert output["username"] == "myusername"
    assert output["is_active"]
    assert len(output['groups']) == 1
    assert state == 201


def test_api_v1users_no_group():
    UserDict = {
      "username": "myusername",
      "password": "mypassword"
    }
    myUser = User(data=UserDict)
    output, state = myUser.create(password="mypassword")

    assert output["error"] == "No groups provided for user."
    assert state == 400


def test_api_v1users_exist():
    groupDict = {
      "name": "mygroupname"
    }
    UserDict = {
      "username": "myusername",
      "password": "mypassword",
      "groups": ["mygroupname"]
    }
    myGroup = Group()
    myUser = User(data=UserDict)
    myGroup.create(data=groupDict)
    myUser.create(password="mypassword")

    myNewUser = User()
    exist = myNewUser.search_by_name(name="myusername")
    assert exist


def test_api_v1users_exist_not():
    myUser = User()
    exist = myUser.search_by_name(name="notexist")
    assert not exist
    

def test_api_v1users_in_group():
    data = {
      "_id": 1234567,
      "username": "myusername",
      "password": "mypassword",
      "groups": ["mygroupname"]
    }
    myUser = User(data=data)
    new_data = myUser.is_in_group(group="mygroupname")
    assert new_data


def test_api_v1users_not_in_group():
    data = {
      "_id": 1234567,
      "username": "myusername",
      "password": "mypassword",
      "groups": ["mygroupname"]
    }
    myUser = User(data=data)
    new_data = myUser.is_in_group(group="mygroupname1")
    assert not new_data


def test_api_v1users_add_to_group():
    UserDict = {
      "username": "myusername",
      "password": "mypassword",
      "groups": ["mygroupname"]
    }
    myUser = User(data=UserDict)
    output, state = myUser.add_to_group(groupname="mygroupname1")
    assert "mygroupname1" in output['groups']
    assert state


def test_api_v1users_remove_from_group():
    UserDict = {
      "username": "myusername",
      "password": "mypassword",
      "groups": ["mygroupname"]
    }
    myUser = User(data=UserDict)
    output, state = myUser.remove_from_group(groupname="mygroupname")

    getOutput, _ = myUser.get()

    assert "" in output
    assert state
    assert 'mygroupname' not in getOutput["groups"]
    assert len(getOutput['groups']) == 0


