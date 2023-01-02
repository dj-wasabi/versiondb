import json

def test_get_artifact_not_exist(test_client, authentication_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/bom/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/api/v1/artifacts/idonotexist', headers=authentication_headers)
    assert response.status_code == 404
    assert response.json == {"error": "Artifact not found."}


def test_create_artifact_wrong_post_data(test_client, authentication_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/bom/' page is requested (GET)
    THEN check the response is valid
    """
    postdict = {
        "name": "artifactname",
        "groups": "wrongkeyname"
    }
    response = test_client.post('/api/v1/artifacts', data=json.dumps(postdict), headers=authentication_headers, follow_redirects=True)

    data = response.json
    assert response.status_code == 400
    assert data["errors"][""] == "Additional properties are not allowed ('groups' was unexpected)"


def test_create_artifact_unauthenticated(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/bom/' page is requested (GET)
    THEN check the response is valid
    """
    postdict = {
        "name": "artifactname",
        "category": "category"
    }
    response = test_client.post('/api/v1/artifacts', data=json.dumps(postdict), headers={'Content-Type': "application/json"}, follow_redirects=True)

    data = response.json
    assert response.status_code == 401


def test_create_artifact(test_client, authentication_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/bom/' page is requested (GET)
    THEN check the response is valid
    """
    postdict = {
        "name": "artifactname",
        "category": "mycategory"
    }
    response = test_client.post('/api/v1/artifacts', data=json.dumps(postdict), headers=authentication_headers, follow_redirects=True)

    data = response.json
    assert response.status_code == 201
    assert data['name'] == "artifactname"
    assert data['version'] == "0.0.0"
    assert data['metadata'] == []


def test_create_artifact_specify_version(test_client, authentication_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/bom/' page is requested (GET)
    THEN check the response is valid
    """
    postdict = {
        "name": "artifactversion",
        "category": "mycategory",
        "version": "0.1.3"
    }
    response = test_client.post('/api/v1/artifacts', data=json.dumps(postdict), headers=authentication_headers, follow_redirects=True)

    data = response.json
    assert response.status_code == 201
    assert data['name'] == "artifactversion"
    assert data['version'] == "0.1.3"
    assert data['metadata'] == []


def test_patch_artifact(test_client, authentication_headers):
    """Update the 'patch' version."""
    response = test_client.post('/api/v1/artifacts/artifactname/patch', headers=authentication_headers, follow_redirects=True)

    data = response.json
    assert response.status_code == 201
    assert data['version'] == "0.0.1"


# def test_patch_artifact_unauthenticated(test_client):
#     """Try to update the 'patch' version while not being authenticated."""
#     response = test_client.post('/api/v1/artifacts/artifactname/patch', headers={'Content-Type': "application/json"}, follow_redirects=True)

#     data = response.json
#     assert data == 123
#     assert response.status_code == 401


def test_patch_artifact_2(test_client, authentication_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/bom/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.post('/api/v1/artifacts/artifactversion/patch', headers=authentication_headers, follow_redirects=True)

    data = response.json
    assert response.status_code == 201
    assert data['version'] == "0.1.4"


def test_get_artifact_get_all_versions(test_client, authentication_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/bom/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/api/v1/artifacts/artifactname/versions', headers=authentication_headers, follow_redirects=True)

    data = response.json
    assert response.status_code == 200
    assert 'versions' in data
    assert data["versions"][0]["version"] == "0.0.0"


# def test_get_artifact_version_not_exist(test_client, authentication_headers):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get('/api/v1/artifacts/artifactname2/version', headers=authentication_headers, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 404
#     assert data['message'] == "Artifact not found."


def test_minor_artifact(test_client, authentication_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/bom/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.post('/api/v1/artifacts/artifactname/minor', headers=authentication_headers)

    data = response.json
    assert response.status_code == 201
    assert data['version'] == "0.1.1"


# def test_minor_artifact_unauthenticated(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.post('/api/v1/artifacts/artifactname/minor', headers={'Content-Type': "application/json"})

#     data = response.json
#     assert response.status_code == 401


def test_major_artifact(test_client, authentication_headers):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/bom/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.post('/api/v1/artifacts/artifactname/major', headers=authentication_headers, follow_redirects=True)

    data = response.json
    assert response.status_code == 201
    assert data['version'] == "1.0.1"


# def test_major_artifact_unauthenticated(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/api/v1/bom/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.post('/api/v1/artifacts/artifactname/major', headers={'Content-Type': "application/json"}, follow_redirects=True)

#     data = response.json
#     assert response.status_code == 401

def test_artifact_get_version(test_client, authentication_headers):
    """Get specific version of artifact."""
    response = test_client.get('/api/v1/artifacts/artifactname/version/0.0.0', headers=authentication_headers)

    data = response.json
    assert response.status_code == 200
    assert data["name"] == "artifactname"
    assert data["version"] == "0.0.0"


def test_artifact_patch_version(test_client, authentication_headers):
    """Get specific version of artifact."""
    patchdict = {
        "shasum": "24cdaecc1acf91894b13fb46fedfd179ea7f88c8"
    }
    response = test_client.patch('/api/v1/artifacts/artifactname/version/0.0.0', data=json.dumps(patchdict), headers=authentication_headers)

    data = response.json
    assert response.status_code == 200
    assert data["name"] == "artifactname"
    assert data["version"] == "0.0.0"
    assert data["shasum"] == "24cdaecc1acf91894b13fb46fedfd179ea7f88c8"


def test_artifact_delete_version(test_client, authentication_headers):
    """Delete specific version of artifact."""
    response = test_client.delete('/api/v1/artifacts/artifactname/version/0.0.1', headers=authentication_headers)
    assert response.status_code == 204
