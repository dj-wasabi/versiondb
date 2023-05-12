import pytest
import os
import json
import sys
import string
import random

from requests import head

currentPath = os.path.dirname(os.path.realpath(__file__))
rootPath = os.path.join(currentPath, "..")
sys.path.append(rootPath)

from api import create_app
from api.server.mongodb.mongodb import client
from api.server.mongodb.initialise import initialise

@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app('ci')
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture
def getRandomName():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))


@pytest.fixture
def dummyArtifactData(getRandomName):
    data = {
        "name": getRandomName,
        "category": getRandomName,
        "url": "https://demo.url"
    }
    return data


@pytest.fixture
def authentication_headers(test_client):
    """Authenticate and return an dictionary with correct headers that can be used for test that requires authentication."""
    postdict = {
        "username": "admin",
        "password": "password"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = test_client.post('/api/v1/users/authenticate', data=json.dumps(postdict), headers=headers)
    data = response.json
    headers["Authorization"] = "Bearer {h}".format(h=data["token"])
    return headers


