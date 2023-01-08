import sys
import os
import pytest


currentPath = os.path.dirname(os.path.realpath(__file__))
rootPath = os.path.join(currentPath, "../..")
sys.path.append(rootPath)
from api.v1artifacts.artifact import Artifact


def test_api_v1artifacts_create_correct(dummyArtifactData):
    artName = dummyArtifactData['name']
    artCategory = dummyArtifactData['category']
    userName = "myUserName"
    myartifact = Artifact(data=dummyArtifactData)
    output, state = myartifact.create(user=userName)

    assert state == 201
    assert output['name'] == artName
    assert output['category'] == artCategory
    assert output['version'] == "0.0.0"


def test_api_v1artifacts_create_incorrect_missing_group(dummyArtifactData):
    dummyArtifactData.pop('category')
    userName = "myUserName"
    myartifact = Artifact(data=dummyArtifactData)
    output, state = myartifact.create(user=userName)

    assert state == 409
    assert output['error'] == "Both 'name' and 'category' are required."


def test_api_v1artifacts_create_incorrect_already_exist(dummyArtifactData):
    userName = "myUserName"

    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)

    myartifact2 = Artifact(data=dummyArtifactData)
    output, state = myartifact2.create(user=userName)

    assert state == 409
    assert output['error'] == "Artifact already exist."


def test_api_v1artifacts_search_by_name(dummyArtifactData):
    userName = "myUserName"
    artName = dummyArtifactData['name']

    myartifact = Artifact()
    result = myartifact.search_by_name(name=artName)

    # Create the artifact so we can search for it.
    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)
    result2 = myartifact.search_by_name(name=artName)
    assert not result
    assert result2


def test_api_v1artifacts_get(dummyArtifactData):
    userName = "myUserName"
    artName = dummyArtifactData['name']

    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)
    output, state = myartifact.get()

    assert state == 200
    assert output['name'] == artName
    assert output['version'] == "0.0.0"


def test_api_v1artifacts_updatePatch(dummyArtifactData):
    userName = "myUserName"
    artName = dummyArtifactData['name']

    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)

    output, state = myartifact.update(name=artName, user=userName, type="patch")
    assert state == 201
    assert output['version'] == "0.0.1"


def test_api_v1artifacts_getNextPatch(dummyArtifactData):
    userName = "myUserName"
    artName = dummyArtifactData['name']

    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)

    output, state = myartifact.getNextVersion(name=artName, type="patch")
    assert state == 200
    assert output['version'] == "0.0.1"


def test_api_v1artifacts_updatePatch_not_exist(dummyArtifactData):
    userName = "myUserName"
    artName = "dummy"

    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)
    output, state = myartifact.update(name=artName, user=userName, type="patch")
    assert state == 404
    assert output['error'] == "Version for provided artifact not found."


def test_api_v1artifacts_updateMinor(dummyArtifactData):
    userName = "myUserName"
    artName = dummyArtifactData['name']

    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)

    output, state = myartifact.update(name=artName, user=userName, type="minor")
    assert state == 201
    assert output['version'] == "0.1.1"


def test_api_v1artifacts_getNextMinor(dummyArtifactData):
    userName = "myUserName"
    artName = dummyArtifactData['name']

    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)

    output, state = myartifact.getNextVersion(name=artName, type="minor")
    assert state == 200
    assert output['version'] == "0.1.1"


def test_api_v1artifacts_updateMinor_not_exist(dummyArtifactData):
    userName = "myUserName"
    artName = "dummy"

    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)
    output, state = myartifact.update(name=artName, user=userName, type="minor")
    assert state == 404
    assert output['error'] == "Version for provided artifact not found."


def test_api_v1artifacts_updateMajor(dummyArtifactData):
    userName = "myUserName"
    artName = dummyArtifactData['name']

    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)

    output, state = myartifact.update(name=artName, user=userName, type="major")
    assert state == 201
    assert output['version'] == "1.0.1"


def test_api_v1artifacts_getNextMajor(dummyArtifactData):
    userName = "myUserName"
    artName = dummyArtifactData['name']

    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)

    output, state = myartifact.getNextVersion(name=artName, type="major")
    assert state == 200
    assert output['version'] == "1.0.1"


def test_api_v1artifacts_updateMajor_not_exist(dummyArtifactData):
    userName = "myUserName"
    artName = "dummy"

    myartifact = Artifact(data=dummyArtifactData)
    _, _ = myartifact.create(user=userName)
    output, state = myartifact.update(name=artName, user=userName, type="major")
    assert state == 404
    assert output['error'] == "Version for provided artifact not found."

