import sys
import os
import pytest


currentPath = os.path.dirname(os.path.realpath(__file__))
rootPath = os.path.join(currentPath, "../..")
sys.path.append(rootPath)
from api.v1groups.group import Group


def test_api_v1groups_search_by_name_not_exist():
    myGroup = Group()
    assert not myGroup.search_by_name(name="dummy")


def test_api_v1groups_create():
    group = {
      "name": "mygroupname"
    }
    myGroup = Group()
    data, state = myGroup.create(data=group)

    assert data["name"] == "mygroupname"
    assert len(data['users']) == 0
    assert state == 201


def test_api_v1groups_create_already_exist():
    group = {
      "name": "mygroupname"
    }
    myGroup = Group()
    myGroup.create(data=group)
    mySecondGroup = Group()
    data, state = mySecondGroup.create(data=group)

    assert state == 409
    assert data['error'] == "The group already exist."


def test_api_v1groups_delete():
    group = {
      "name": "mygroupname"
    }
    myGroup = Group()
    myGroup.create(data=group)

    mySecondGroup = Group()
    mySecondGroup.search_by_name(name="mygroupname")
    data, state = mySecondGroup.delete()

    assert state == 204
    assert data == {}
